stl = """
QTabWidget::tab-bar {
    left: 2px; /* move to the right by 2px */
}

/* Style the tab using the tab sub-control. Note that
 * it reads QTabBar _not_ QTabWidget
 */
QTabBar::tab {
    min-width: 15px;
    max-width: 240px;
    padding: 4px 16px;
    font-size: .85em;
}

QTabBar::tab:!selected {
    margin-top: 3px; /* make non-selected tabs look smaller */
}

/* make use of negative margins for overlapping tabs */
QTabBar::tab:selected {
    /* expand/overlap to the left and right by 4px */
    margin-left: -2px;
    margin-right: -2px;
}

QTabBar::tab:first:selected {
    /* first selected tab has nothing to overlap with on the left */
    margin-left: 0;
}

QTabBar::tab:last:selected {
    /* last selected tab has nothing to overlap with on the right */
    margin-right: 0;
}

QTabBar::tab:only-one {
    /* if there is only one tab, we don't want overlapping margins */
    margin-left: 0;
    margin-right: 0;
}
"""

dtl = """
QDockWidget {
     border: 1px solid lightgray;
     titlebar-close-icon: url(close.png);
     titlebar-normal-icon: url(undock.png);
 }

 QDockWidget::title {
     text-align: left; /* align the text to the left */
     background: lightgray;
     padding-left: 5px;
 }

 QDockWidget::close-button, QDockWidget::float-button {
     border: 1px solid transparent;
     background: darkgray;
     padding: 0px;
 }

 QDockWidget::close-button:hover, QDockWidget::float-button:hover {
     background: gray;
 }

 QDockWidget::close-button:pressed, QDockWidget::float-button:pressed {
     padding: 1px -1px -1px 1px;
 }
"""

ttl = """
QToolBar {
     //background: black;
     spacing: 3px; /* spacing between items in the tool bar */
 }

 QToolBar::handle {
     //image: url(handle.png);
 }
"""
statl = """
QStatusBar {
     background: brown;
 }

 QStatusBar::item {
     border: 1px solid red;
     border-radius: 3px;
 }
"""

scl = """
QScrollBar:horizontal {
     border: 2px solid grey;
     background: #32CC99;
     height: 15px;
     margin: 0px 20px 0 20px;
 }
 QScrollBar::handle:horizontal {
     background: white;
     min-width: 20px;
 }
 QScrollBar::add-line:horizontal {
     border: 2px solid grey;
     background: #32CC99;
     width: 20px;
     subcontrol-position: right;
     subcontrol-origin: margin;
 }

 QScrollBar::sub-line:horizontal {
     border: 2px solid grey;
     background: #32CC99;
     width: 20px;
     subcontrol-position: left;
     subcontrol-origin: margin;
 }
"""