from .running_stitch import RunningStitchLayer

_layer_classes = [RunningStitchLayer]
__all__ = ["RunningStitchLayer"]
by_id = {}

for layer_class in _layer_classes:
    by_id[layer_class.layer_id] = layer_class
