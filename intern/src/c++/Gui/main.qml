import QtQuick 2.13
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.0
import QtQuick.Window 2.13

import com.myself 1.0

Window {
    id: mainWindow
    visible: true
    width: 800
    height: 600
    title: qsTr("Prozedurale Verteilung von Gestrüpp")

    Rectangle {
        id: menu
        x: 0
        y: 0
        width: 800
        height: 52
        color: "#ffffff"
        border {
            width: 2
            color: "black"
        }

        Rectangle {
            id: load_image
            x: 0
            y: 0
            width: parent.height
            height: parent.height
            color: "#ffffff"

            border {
                width: 1
                color: "black"
            }

            Text {
                id: element
                width: parent.width
                height: parent.height
                text: qsTr("Load Image")
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                font.pixelSize: 12
            }

            MouseArea {
                id: mouseArea
                x: 0
                y: 0
                width: parent.width
                height: parent.height

                onClicked: {
                    fileDialog.open()
                }
            }
        }
    }

    Rectangle {
        id: heightmap_frame
        x: 0
        y: menu.height
        width: mainWindow.width/2
        height: mainWindow.height/2
        color: "#ffffff"

        border {
            width: 2
            color: "black"
        }

        // components
        Text {
            width: parent.width
            height: 20
            text: "Height-Map"
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 12
        }

        Rectangle {
            id: heightmap
            color: "#ffffff"
            y: 20
            width: parent.width
            height: parent.height-20
            border {
                width: 2
                color: "black"
            }

            Image {
                id: heightMapImage
                width: parent.width
                height: parent.height
                source: ""
                fillMode: Image.PreserveAspectFit
            }
        }
    }

    Rectangle {
        id: insolation_frame
        x: 400
        y: menu.height
        width: mainWindow.width/2
        height: mainWindow.height/2
        color: "#ffffff"
        border.color: "#000000"

        Text {
            width: parent.width
            height: 20
            text: "Calculated insolation"
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
        }

        Rectangle {
            id: insolation
            y: 20
            width: parent.width
            height: parent.height-20
            color: "#ffffff"
            border.color: "#000000"
            border.width: 2
        }

        Rectangle {
            id: calculate_insolation
            x: 100
            y: 400
            width: 200
            height: 37
            color: "#ffffff"
            radius: 0
            border.width: 2

            CInsolation {
                id: isolation_object
            }

            CImageLoader {
                id: image_loader
            }

            Text {
                id: element1
                x: 0
                y: 0
                width: parent.width
                height: parent.height
                text: qsTr("Calculate insolation")
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 12
            }

            MouseArea {
                id: mouseArea1
                x: 0
                y: 0
                width: parent.width
                height: parent.height

                onClicked: {
                    console.log(heightMapImage.source)
                    image_loader.LoadImage(heightMapImage.source)
                }
            }
        }
        border.width: 2
    }

    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        folder: shortcuts.home

        nameFilters: [ "Image files (*.jpg *.png)", "All files (*)" ]

        onAccepted: {
            console.log("You chose: " + fileDialog.fileUrls)
            heightMapImage.source = fileDialog.fileUrls[0]
            //Qt.quit()
        }

        onRejected: {
            console.log("Canceled")
            //Qt.quit()
        }
        Component.onCompleted: visible = false
    }
}
