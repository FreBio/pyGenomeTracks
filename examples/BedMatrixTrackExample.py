import numpy as np
from pygenometracks.tracksClass import BedGraphTrack
from pygenometracks.tracksClass import GenomeTrack


class BedGraphMatrixExample(BedGraphTrack):
    SUPPORTED_ENDINGS = ['.bm', '.bm.gz' '.bedgraphmatrix']
    TRACK_TYPE = 'bedgraph_matrix'
    OPTIONS_TXT = GenomeTrack.OPTIONS_TXT + """
        # a bedgraph matrix file is like a bedgraph, except that per bin there
        # are more than one value separated by tab: E.g.
        # This file type is produced by HiCExplorer tool hicFindTads and contains
        # the TAD-separation score at different window sizes
        # chrX	18279	40131	0.399113	0.364118	0.320857	0.274307
        # chrX	40132	54262	0.479340	0.425471	0.366541	0.324736
        #min_value = 0.10
        #max_value = 0.70
        # if type is set as lines, then the TAD score lines are drawn instead
        # of the matrix otherwise a heatmap is plotted
        type = lines
        #plot horizontal lines=False
        file_type = {}
            """.format(TRACK_TYPE)

    def plot(self, ax, label_ax, chrom_region, start_region, end_region):
        """

        :param ax:
        :param label_ax:
        :param chrom_region:
        :param start_region:
        :param end_region:
        :return:
        """

        start_pos = []
        matrix_rows = []

        for region in sorted(self.interval_tree[chrom_region][start_region - 10000:end_region + 10000]):
            start_pos.append(region.begin)
            values = map(float, region.data)
            matrix_rows.append(values)

        matrix = np.vstack(matrix_rows).T
        x, y = np.meshgrid(start_pos, np.arange(matrix.shape[0]))
        shading = 'gouraud'
        vmax = self.properties['max_value']
        vmin = self.properties['min_value']

        img = ax.pcolormesh(x, y, matrix, vmin=vmin, vmax=vmax, shading=shading)
        img.set_rasterized(True)

        label_ax.text(0.15, 0.5, self.properties['title'])