import QtQuick 2.12
import QtQuick.Controls 2.5

Page {
    id: page
    //anchors.fill: parent
    //width: 1280
    //height: 720

    title: qsTr("Login")
    Rectangle {
        id: rectangle
        width: 401
        height: 589
        color: "#a9a9a9"
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        Label {
            id: label2
            x: 309
            y: 263
            color: "#ffffff"
            text: qsTr("Senha")
            styleColor: "#ffffff"
            anchors.horizontalCenterOffset: 0
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: 20
        }

        TextField {
            id: textFieldUser
            x: 271
            y: 146
            width: 213
            height: 60
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: 18
            selectByMouse: true
        }

        TextField {
            id: textFieldPassword
            x: 272
            y: 346
            width: 208
            height: 60
            anchors.horizontalCenterOffset: 2
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: 18
            echoMode: TextInput.Password
            selectByMouse: true
        }

        Button {
            id: button
            x: 111
            y: 504
            width: 149
            height: 57
            text: qsTr("Entrar")
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: 18
            font.preferShaping: true
            font.kerning: true
            font.family: "Arial"
            checked: false
            checkable: false
            font.capitalization: Font.Capitalize
            focusPolicy: Qt.NoFocus

            onClicked:{
                loginController.login(textFieldUser.text, textFieldPassword.text)
            }
        }

        Label {
            id: label1
            x: 312
            y: 65
            width: 121
            height: 50
            color: "#ffffff"
            text: qsTr("Usuário")
            anchors.horizontalCenter: parent.horizontalCenter
            verticalAlignment: Text.AlignTop
            horizontalAlignment: Text.AlignHCenter
            font.pointSize: 20
        }
    }
/*
    RoundButton {
        id: roundButton
        y: 605
        width: 75
        height: 75
        text: "C"
        font.preferShaping: true
        font.capitalization: Font.MixedCase
        font.pointSize: 10
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 33
        anchors.left: parent.left
        anchors.leftMargin: 50
        wheelEnabled: false
        spacing: 7
        autoExclusive: false
        autoRepeat: false
        flat: false
        highlighted: false
        font.bold: true
        display: AbstractButton.TextBesideIcon
        focusPolicy: Qt.StrongFocus

        //background: Rectangle {
        //color: "#8B008B"
        //radius: 28
        //}
    }
*/
}


