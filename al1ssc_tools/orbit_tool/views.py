from django.http import JsonResponse
import numpy as np
from sunpy.coordinates.ephemeris import get_horizons_coord
from sunpy.coordinates import frames
from datetime import timedelta

from .models import Body
from .orbit_plotter_2D import HeliosphericConstellation


def get_bodies(request):
    data = list(Body.objects.values())
    return JsonResponse(data, safe=False)


def get_2Dorbit_plot(request):
    if request.method == "GET":
        queryDict = request.GET
        time = queryDict.__getitem__("time")
        bodies_list = queryDict.getlist("bodies[]")
        vsw_list = list(map(int, queryDict.getlist("vsw[]")))
        plot_spirals = to_bool(queryDict.__getitem__("spirals"))
        plot_sun_body_line = to_bool(queryDict.__getitem__("sbLine"))
        show_earth_centered_coord = to_bool(queryDict.__getitem__("coordE"))
        reference_long = to_int(queryDict.get("refLong", None))
        reference_lat = to_int(queryDict.get("refLat", None))
        reference_vsw = to_int(queryDict.get("refVsw", 400))

        # TODO: Validate params
        # compare length of bodies with vsw and that both are not 0
        # if reference long is passed, lat & vsw must also be

        hc = HeliosphericConstellation(
            time, bodies_list, vsw_list, reference_long, reference_lat
        )
        img_as_base64 = hc.plot(
            plot_spirals,
            plot_sun_body_line,
            show_earth_centered_coord,
            reference_vsw,
        )
        tabular_data = hc.coord_table.to_dict("records")  # list of dictionaries

        return JsonResponse(
            dict(
                plot=f"data:image/png;base64,{img_as_base64}",
                table=tabular_data,
            )
        )


def get_3Dorbit_data(request):
    if request.method == "GET":
        params = request.GET.dict()
        # TODO: Validate params
        time_period = {
            "start": params["timeStart"],
            "stop": params["timeStop"],
            "step": params["timeStep"],
        }
        body_name = params["body"]
        body_id = Body.objects.get(name=body_name).body_id

        coord = get_horizons_coord(
            body=body_id,
            time=time_period,
            id_type="id",
        ).transform_to(frames.HeliocentricInertial)
        x, y, z = coord.cartesian.xyz.value  # in AU
        # obstime is in tdb, convert it to utc and round off
        utc_obstime_str = np.array(
            [rounded_datetime_str(d) for d in coord.obstime.utc.datetime]
        )
        hovertemplate = (
            "<b>%{customdata[0]} UTC</b>"
            + "<br>x: %{x} AU<br>y: %{y} AU<br>z: %{z} AU"
            + "<br>lon.: %{customdata[1]:.3f}°"
            + "<br>lat.: %{customdata[2]:.3f}°"
            + "<br>dist.: %{customdata[3]:.3f} AU"
        )
        customdata = np.stack(
            (
                utc_obstime_str,
                np.around(coord.lon.value, 3),
                np.around(coord.lat.value, 3),
                np.around(coord.distance.value, 3),  # in AU
            ),
            axis=-1,
        )
        color = Body.objects.get(name=body_name).color

        return JsonResponse(
            dict(
                x=np.around(x, 6).tolist(),
                y=np.around(y, 6).tolist(),
                z=np.around(z, 6).tolist(),
                hovertemplate=hovertemplate,
                customdata=customdata.tolist(),
                name=body_name,
                color=color,
            )
        )


def rounded_datetime_str(d):
    d_rounded_to_minute = d + timedelta(minutes=d.second // 30)
    return (d_rounded_to_minute).strftime("%Y-%m-%d %H:%M")


def to_bool(bool_str):
    if bool_str == "true":
        return True
    elif bool_str == "false":
        return False
    else:
        raise TypeError("Only 'true' or 'false' are allowed!")


def to_int(int_str):
    try:
        return int(int_str)
    except TypeError:
        return int_str
