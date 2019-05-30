import QtQuick 2.12
import QtQuick.Controls 2.5

Page {
    id: page
    //width: 1280
    //height: 720
    anchors.fill: parent

    title: "Eventos"
    ListView {
        id: listViewActions
        x: 433
        width: 503
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 50
        anchors.top: parent.top
        anchors.topMargin: 50
        anchors.horizontalCenter: parent.horizontalCenter
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
                    MouseArea{
                        anchors.fill:parent
                        z: 1
                        hoverEnabled: false

                        onClicked:{
                            controller.clickedEvent(rectangle)
                        }
                    }

            

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
            
            id: sampleModel
            objectName:"batata"
            function apendous(newElement) {
                sampleModel.append(newElement)
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

        onClicked: {
            controller.addEvent()
        }
    }
}
