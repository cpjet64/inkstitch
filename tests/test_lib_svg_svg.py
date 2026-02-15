from lib.svg.svg import point_upwards

import pytest
from inkex import Rectangle, Transform, PathElement
from inkex.tester.svg import svg


class TestLibSvgSvg:
    def _assert_transform_close(
        self,
        actual: Transform,
        expected: Transform,
        decimals: int,
    ) -> None:
        tolerance = 10 ** (-decimals)
        assert list(actual.to_hexad()) == pytest.approx(
            list(expected.to_hexad()),
            abs=tolerance,
        )

    def test_point_upwards(self) -> None:
        root = svg()
        rect = root.add(Rectangle(attrib={"width": "10", "height": "10", "x": "10", "y": "20"}))
        rect.transform = Transform().add_rotate(-45)

        point_upwards(rect)

        self._assert_transform_close(
            rect.transform,
            Transform().add_translate(Transform().add_rotate(-45).apply_to_point((10, 20))),
            4,
        )

    def test_point_upwards_mirrored(self) -> None:
        root = svg()
        rect = root.add(
            PathElement(
                attrib={
                    "d": "M 0,0 L 10,0 0,5 Z",
                }
            )
        )
        rect.transform = Transform().add_rotate(-45).add_scale(-1, 1)

        point_upwards(rect)

        self._assert_transform_close(
            rect.transform,
            Transform(),
            4,
        )
