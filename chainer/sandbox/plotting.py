# -*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import chainer

import  bokeh.plotting as plotting
from bokeh.models import GlyphRenderer


class LiveMonitor(object):

    def __init__(self, server='chainer', url='http://localhost:5006/', **kwargs):

        plotting.output_server(server, url=url)

        # 各サブプロットを作成
        self.train_loss = self._init_figure(title='Train loss', color='#FF0000', **kwargs)
        self.train_acc = self._init_figure(title='Train accuracy', color='#0000FF', **kwargs)
        self.test_loss = self._init_figure(title='Test loss',  color='#FF0000', **kwargs)
        self.test_acc = self._init_figure(title='Test accuracy', color='#0000FF', **kwargs)

        # 作成したサブプロットを grid 上にレイアウト
        self.grid = plotting.gridplot([[self.train_loss, self.test_loss],
                                       [self.train_acc, self.test_acc]])

        # grid を描画
        plotting.show(self.grid)

    def _init_figure(self, color=None, line_width=2,
                     title=None, title_text_font_size='9pt',
                     plot_width=400, plot_height=280):
        """サブプロットの初期化"""
        figure = plotting.figure(title=title, title_text_font_size=title_text_font_size,
                                 plot_width=plot_width, plot_height=plot_height)
        x = np.array([])
        y = np.array([])
        # figure に空の折れ線グラフを追加
        figure.line(x, y, color=color, line_width=line_width)
        return figure

    def _maybe_update(self, figure, value):
        if value is not None:
            if isinstance(value, chainer.Variable):
                import chainer.cuda as cuda
                value = cuda.to_cpu(value.data)
            print(value)
            # figure の data_source を取得
            renderer = figure.select(dict(type=GlyphRenderer))
            ds = renderer[0].data_source
            # data_source の値を更新すると、プロットも更新される
            y = np.append(ds.data['y'], value)
            x = np.arange(len(y))
            ds.data['y'] = y
            ds.data['x'] = x
            plotting.cursession().store_objects(ds)

    def update(self, train_loss=None, train_accuracy=None,
               test_loss=None, test_accuracy=None):
        self._maybe_update(self.train_loss, train_loss)
        self._maybe_update(self.train_acc, train_accuracy)
        self._maybe_update(self.test_loss, test_loss)
        self._maybe_update(self.test_acc, test_accuracy)
