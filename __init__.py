from binaryninja import *
import json

class FunctionDump(BackgroundTaskThread):
    def __init__(self, msg, bv):
        BackgroundTaskThread.__init__(self, msg, True)
        self.bv = bv

    def run(self):
        j = {}
        j["functions"] = []

        for function in self.bv.functions:
            addr = function.address_ranges[0].start
            j["functions"].append( {"name" : function.name, "addr" : addr} )

        out_path = binaryninja.interaction.get_save_filename_input("Save JSON file", ext="*.json")

        if out_path is not None:
            if len(out_path) > 5:
                if out_path[-5:] != ".json":
                    out_path += ".json"

            with open(out_path, "w+") as f:
                f.write(str(json.dumps(j)))

def dump_functions(bv):
    task = FunctionDump("Dumping functions", bv)
    task.run()

PluginCommand.register("Dump Functions to JSON", "", dump_functions)