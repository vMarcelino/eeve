import QtQuick 2.12
import QtQuick.Controls 2.5

Page {
    id: page
    //width: 1280
    //height: 720
    anchors.fill: parent

    title: "Editar Evento"
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
                    text: "Gatilho 1"
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    font.bold: true
                    font.pointSize: 13
                }

                PressAndHoldButton {
                    anchors.right: rectangle2.right
                    //text: "X"
                    source: "open-file.png"
                    anchors.verticalCenter: parent.verticalCenter
                    width: 35
                    height: 35
                }
            }
        }

        ListView {
            id: listViewActions
            x: 0
            y: 79
            width: 504
            height: 556
            delegate: Item {
                id: element
                x: 5
                width: listViewActions.width
                height: 55
                clip: true
                Row {
                    id: row1
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 10
                    //width: listView.width
                    Rectangle {
                        width: listViewActions.width
                        height: 40
                        id: rectangle
                        color: colorCode

                        Text {
                            //id: name
                            text: name
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.verticalCenter: parent.verticalCenter
                            font.bold: true
                        }

                        Row {
                            id: row
                            anchors.right: rectangle.right
                            anchors.verticalCenter: parent.verticalCenter

                            Switch {
                                //source: "content/pics/plus-sign.png"
                                //onClicked: fruitModel.setProperty(index, "cost", cost + 0.25)
                            }

                            PressAndHoldButton {
                                //text: "X"
                                source: "list-delete.png"
                                anchors.verticalCenter: parent.verticalCenter
                                //width: 40
                                //height: 40
                            }
                        }
                    }
                }
            }
            model: ListModel {
                ListElement {
                    name: "Ação 1"
                    colorCode: "#DDA0DD"
                }

                ListElement {
                    name: "Ação 2"
                    colorCode: "#DDA0DD"
                }

                ListElement {
                    name: "Ação 3"
                    colorCode: "#DDA0DD"
                }
            }
        }
    }
    RoundButton {
        id: roundButton
        x: 1131
        y: 587
        width: 75
        height: 75
        text: "+"
        anchors.right: parent.right
        anchors.rightMargin: 73
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 58
    }
}
