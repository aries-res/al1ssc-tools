from django.http import JsonResponse
import numpy as np
from sunpy.coordinates.ephemeris import get_horizons_coord
from sunpy.coordinates import frames
from datetime import timedelta

from .models import Body


def get_bodies(request):
    data = list(Body.objects.values())
    return JsonResponse(data, safe=False)


def get_3Dorbit_data(request):
    if request.method == "GET":
        params = request.GET.dict()
        # TODO: Validate params
        time_period = {
            "start": params["timeStart"],
            "stop": params["timeStop"],
            "step": params["timeStep"],
        }
        body_id = params["body"]

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
        # TODO: Add units in hoverlabel
        hovertemplate = (
            "<b>%{customdata[0]}</b>"
            + "<br>x: %{x}<br>y: %{y}<br>z: %{z}"
            + "<br>lon: %{customdata[1]: .6f}"
            + "<br>lat: %{customdata[2]: .6f}"
            + "<br>distance: %{customdata[3]: .6f}"
        )
        customdata = np.stack(
            (
                utc_obstime_str,
                coord.lon.value,
                coord.lat.value,
                coord.distance.value,  # in AU
            ),
            axis=-1,
        )
        name = Body.objects.get(body_id=body_id).name

        return JsonResponse(
            dict(
                x=x.tolist(),
                y=y.tolist(),
                z=z.tolist(),
                hovertemplate=hovertemplate,
                customdata=customdata.tolist(),
                name=name,
            )
        )


def rounded_datetime_str(d):
    d_rounded_to_minute = d + timedelta(minutes=d.second // 30)
    return (d_rounded_to_minute).strftime("%Y-%m-%d %H:%M")
