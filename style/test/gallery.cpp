// Renders a widget gallery with the Haiku style to a PNG (offscreen-capable).
#include "haikustyle.h"
#include <QApplication>
#include <QtWidgets>

int main(int argc, char **argv)
{
    QApplication app(argc, argv);
    auto *style = new HaikuStyle;
    app.setStyle(style);
    app.setPalette(style->standardPalette());

    QMainWindow win;
    auto *mb = win.menuBar();
    mb->addMenu("&File"); mb->addMenu("&Edit"); mb->addMenu("&View"); mb->addMenu("&Help");
    auto *central = new QWidget; auto *grid = new QGridLayout(central);

    auto *b1 = new QPushButton("OK"); b1->setDefault(true);
    auto *b2 = new QPushButton("Cancel");
    auto *b3 = new QPushButton("Disabled"); b3->setEnabled(false);
    auto *b4 = new QPushButton("Pressed"); b4->setDown(true);
    auto *hb = new QHBoxLayout; hb->addWidget(b1); hb->addWidget(b2); hb->addWidget(b3); hb->addWidget(b4);
    grid->addLayout(hb, 0, 0, 1, 2);

    auto *cbx = new QGroupBox("Options"); auto *v = new QVBoxLayout(cbx);
    auto *c1 = new QCheckBox("Checked"); c1->setChecked(true);
    auto *c2 = new QCheckBox("Unchecked");
    auto *c3 = new QCheckBox("Tristate"); c3->setTristate(true); c3->setCheckState(Qt::PartiallyChecked);
    auto *r1 = new QRadioButton("Radio on"); r1->setChecked(true);
    auto *r2 = new QRadioButton("Radio off");
    for (auto *x : {(QWidget*)c1,(QWidget*)c2,(QWidget*)c3,(QWidget*)r1,(QWidget*)r2}) v->addWidget(x);
    grid->addWidget(cbx, 1, 0);

    auto *f = new QWidget; auto *fl = new QFormLayout(f);
    fl->addRow("Name:", new QLineEdit("Haiku"));
    auto *cb = new QComboBox; cb->addItems({"BeOS", "Haiku"}); fl->addRow("Menu field:", cb);
    auto *ecb = new QComboBox; ecb->setEditable(true); ecb->addItem("editable"); fl->addRow("Editable:", ecb);
    auto *sp = new QSpinBox; sp->setValue(42); fl->addRow("Spin:", sp);
    auto *sl = new QSlider(Qt::Horizontal); sl->setValue(60); sl->setTickPosition(QSlider::TicksBelow); sl->setTickInterval(10); fl->addRow("Slider:", sl);
    auto *pb = new QProgressBar; pb->setValue(65); fl->addRow("Progress:", pb);
    grid->addWidget(f, 1, 1);

    auto *tabs = new QTabWidget;
    auto *tree = new QTreeWidget; tree->setHeaderLabels({"Name", "Size", "Modified"});
    for (int i = 0; i < 40; ++i) {
        auto *it = new QTreeWidgetItem(tree, {QString("Item %1").arg(i), "4 KiB", "today"});
        new QTreeWidgetItem(it, {"child"});
    }
    tree->topLevelItem(0)->setExpanded(true);
    tree->setCurrentItem(tree->topLevelItem(2));
    tabs->addTab(tree, "Files"); tabs->addTab(new QTextEdit, "Text"); tabs->addTab(new QWidget, "More");
    grid->addWidget(tabs, 2, 0, 1, 2);

    auto *tb = win.addToolBar("tb");
    tb->addAction(app.style()->standardIcon(QStyle::SP_DirOpenIcon), "Open");
    tb->addAction(app.style()->standardIcon(QStyle::SP_DialogSaveButton), "Save");

    win.setCentralWidget(central);
    win.resize(620, 560);
    win.show();
    QTimer::singleShot(300, [&] {
        win.grab().save(argc > 1 ? argv[1] : "gallery.png");
        app.quit();
    });
    return app.exec();
}
