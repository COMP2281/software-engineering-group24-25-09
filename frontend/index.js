import { app, BrowserWindow } from 'electron'
/*global console*/
import { spawn } from 'child_process'
import rq from 'request-promise'
import portfinder from 'portfinder'

app.commandLine.appendSwitch('disable-http-cache')
// app.whenReady().then(() => {
//     createWindow()
// })

app.on('window-all-closed', function () {
    //if (process.platform != 'darwin') {
    app.quit()
    //}
})

app.on('ready', function () {
    // call python?
    //var subpy = require('child_process').spawn('./dist/hello.exe');
    portfinder.getPort(function (_err, port) {
        console.log(port)
        var subpy = spawn('python', ['server.py', port], { cwd: '..', stdio: 'inherit' })
        var mainAddr = 'http://localhost:' + port
        var openWindow = function () {
            const mainWindow = new BrowserWindow({ width: 800, height: 600 })
            // mainWindow.loadURL('file://' + __dirname + '/index.html');
            mainWindow.loadURL(mainAddr)
            mainWindow.on('closed', function () {
                subpy.kill('SIGINT')
            })
        }
        var startUp = function () {
            rq(mainAddr)
                .then(function () {
                    console.log('server started!')
                    openWindow()
                })
                .catch(function () {
                    // console.log('waiting for the server start...');
                    startUp()
                })
        }

        startUp()
    })
})
