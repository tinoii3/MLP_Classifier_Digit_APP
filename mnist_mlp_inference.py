import json
import h5py
import numpy as np


def _find_kernel_bias(layer_group):
    kernel = bias = None

    def visit(g):
        nonlocal kernel, bias
        for k in g.keys():
            obj = g[k]
            if isinstance(obj, h5py.Dataset):
                if k == "kernel":
                    kernel = np.asarray(obj, dtype=np.float32)
                elif k == "bias":
                    bias = np.asarray(obj, dtype=np.float32)
            else:
                visit(obj)

    visit(layer_group)
    if kernel is None or bias is None:
        raise ValueError("Could not find kernel/bias in Keras layer group")
    return kernel, bias


def _dense_layer_names_from_config(f):
    if "model_config" not in f.attrs:
        return None
    raw = f.attrs["model_config"]
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    cfg = json.loads(raw)
    names = []
    for layer in cfg.get("config", {}).get("layers", []):
        if layer.get("class_name") == "Dense":
            names.append(layer["config"]["name"])
    return names if names else None


def load_keras_dense_stack(h5_path):
    weights = []
    with h5py.File(h5_path, "r") as f:
        if "model_weights" not in f:
            raise ValueError("Expected Keras HDF5 with 'model_weights'")
        mw = f["model_weights"]
        names = _dense_layer_names_from_config(f)
        if not names:
            candidates = []
            for n in mw.keys():
                if n == "dense":
                    candidates.append(n)
                elif n.startswith("dense_") and n[6:].isdigit():
                    candidates.append(n)
            names = sorted(candidates, key=lambda n: 0 if n == "dense" else int(n.split("_")[1]))
        for name in names:
            weights.append(_find_kernel_bias(mw[name]))
    return weights


def _softmax(logits):
    x = logits - np.max(logits, axis=-1, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=-1, keepdims=True)


def predict_mlp(weights, x):
    single = x.ndim == 1
    if single:
        x = x[np.newaxis, :]
    h = x
    for kernel, bias in weights[:-1]:
        h = np.maximum(0.0, h @ kernel + bias)
    kernel, bias = weights[-1]
    logits = h @ kernel + bias
    out = _softmax(logits)
    return out[0] if single else out


class MNISTMLP:
    def __init__(self, h5_path):
        self._weights = load_keras_dense_stack(h5_path)

    def predict(self, x, verbose=0, **kwargs):
        del verbose, kwargs
        x = np.asarray(x, dtype=np.float32)
        return predict_mlp(self._weights, x)
