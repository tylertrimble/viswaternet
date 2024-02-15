import matplotlib.pyplot as plt
import os


def save_fig(self, save_name=None, dpi='figure', save_format='png'):
    model = self.model
    networkName = model["inp_file"]

    if networkName.endswith(".inp"):

        try:

            prefixRemove = networkName.rfind("/")
            if prefixRemove == -1:
                prefixRemove = networkName.rfind("\\")

            networkName = networkName[prefixRemove + 1:]
        except Exception:

            pass
        networkName = networkName[:-4]
        networkName = networkName+"."+save_format
    if save_name is not None:

        file_name = str(save_name) + networkName
    else:

        file_name = networkName

    image_path_full = os.path.join(os.getcwd(), file_name)
    plt.savefig(image_path_full, dpi=dpi,
                format=save_format, bbox_inches="tight")
