/*global console*/
import { app, BrowserWindow } from 'electron'
import { spawn } from 'child_process'
import rq from 'request-promise'
import portfinder from 'portfinder'
import path from 'path';
import { fileURLToPath } from 'url';

const dir = path.dirname(fileURLToPath(import.meta.url));

app.commandLine.appendSwitch('disable-http-cache')

app.on('window-all-closed', function () {
    app.quit()
})

app.on('ready', function () {
    portfinder.getPort(function (_err, port) {
        console.log(port)
        var subpy = spawn('python', ['server.py', dir + '/frontend', port], { cwd: dir + '/backend', stdio: 'inherit' })
        var mainAddr = 'http://localhost:' + port
        var openWindow = function () {
            const mainWindow = new BrowserWindow({ width: 800, height: 600 })
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
                    startUp()
                })
        }

        startUp()
    })
})
