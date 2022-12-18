"""
The viswaternet.utils.save_fig module saves figures generated by viswaternet.
"""
import matplotlib.pyplot as plt
import os


def save_fig(self, save_name=None, dpi='figure', save_format='png'):
    """Saves figure to the directory specified in model["image_path"].

    Arguments
    ---------
    save_name : string
        The inputted string will be appended to the name of the network.

        Example
        -------
        >>>import viswaternet as vis
        >>>model = vis.VisWNModel(r'Networks/Net3.inp')
        ...
        >>>model.save_fig(save_name='_example')
        <Net3_example.png>

    dpi : int, string
        The dpi that the figure will be saved with.

    save_format : string
        The file format that the figure will be saved as.
    """

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
