#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QtWidgets/QLabel>

#include "Logic/logic_image_loader.h"
#include "Logic/logic_insolation.h"

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    QGuiApplication app(argc, argv);
    qmlRegisterType<Logic::CInsolation>("com.myself", 1, 0, "CInsolation");
    qmlRegisterType<Logic::CImageLoader>("com.myself", 1, 0, "CImageLoader");

    QQmlApplicationEngine engine;
    const QUrl url("qrc:///intern/src/c++/Gui/main.qml");
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url](QObject *obj, const QUrl &objUrl) {
                if (!obj && url == objUrl)
                    QCoreApplication::exit(-1);
            }, Qt::QueuedConnection);
    engine.load(url);

    return app.exec();
}