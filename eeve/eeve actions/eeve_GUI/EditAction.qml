import QtQuick 2.12
import QtQuick.Controls 2.5

Page {
    id: page
    //width: 1280
    //height: 720
    anchors.fill: parent

    title: "Editar Ação"

    Rectangle {
        color: "transparent"
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 35
        anchors.top: parent.top
        anchors.topMargin: 50
        anchors.horizontalCenterOffset: 0
        anchors.horizontalCenter: parent.horizontalCenter
        width: 503
        id: container
        x: 433

        Item {
            id: element1
            x: 397
            width: 504
            anchors.margins: 20

            Rectangle {
                width: element1.width
                height: 55
                id: rectangle2
                x: -392
                y: 0
                color: "#DDA0DD"

                Text {
                    //id: name
                    text: "Ação 1"
                    font.pointSize: 13
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    font.bold: true
                }

                PressAndHoldButton {
                    anchors.right: rectangle2.right
                    //text: "X"
                    source: "/open-file.png"
                    anchors.verticalCenter: parent.verticalCenter
                    width: 35
                    height: 35
                }
            }
        }

        Label {
            id: label
            x: 34
            y: 148
            text: qsTr("Parametro 1")
            font.pointSize: 18
        }

        TextField {
            id: textField
            x: 228
            y: 148
            width: 233
            height: 43
            text: qsTr("")
        }

        TextField {
            id: textField1
            x: 228
            y: 222
            width: 233
            height: 43
            text: qsTr("")
        }

        Label {
            id: label1
            x: 34
            y: 224
            text: qsTr("Parametro 2")
            font.pointSize: 18
        }
    }
}

