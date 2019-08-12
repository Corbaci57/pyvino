
import os
from openvino.inference_engine import IENetwork, IEPlugin
from vinopy.util.config import (DEVICE, MODEL_DIR, MODEL_FP,
                                CPU_EXTENSION, TASKS)


class Model(object):
    # TODO: load from config
    def __init__(self, task):
        self.task = task
        self.device = DEVICE
        self._set_model_path()
        # Read IR
        self.net = IENetwork(model=self.model_xml, weights=self.model_bin)
        # Load Model
        self._set_ieplugin()
        self._get_io_blob()

    def _set_ieplugin(self):
        plugin = IEPlugin(device=self.device, plugin_dirs=None)
        if DEVICE == "CPU":
            plugin.add_cpu_extension(CPU_EXTENSION)
        self.exec_net = plugin.load(network=self.net, num_requests=2)

    def _set_model_path(self):
        model_name = TASKS[self.task]
        path_model_dir = os.path.join(MODEL_DIR, model_name, MODEL_FP)

        self.model_xml = os.path.join(
            path_model_dir, model_name + '.xml')
        self.model_bin = os.path.join(
            path_model_dir, model_name + ".bin")

    def _get_io_blob(self):
        self.input_blob = next(iter(self.net.inputs))
        self.out_blob = next(iter(self.net.outputs))