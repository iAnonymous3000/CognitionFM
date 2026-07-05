"""Recipe generators. A recipe YAML names a generator; the generator turns the
YAML's evidence-derived parameters into a sorted Event list."""

from . import ambient_layers, pulse_layers

GENERATORS = {
    "ambient_layers": ambient_layers.generate,
    "pulse_layers": pulse_layers.generate,
}
