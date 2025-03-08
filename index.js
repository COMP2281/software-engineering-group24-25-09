import { app, BrowserWindow } from 'electron'
import { spawn } from 'child_process'
import fetch from 'node-fetch'
import portfinder from 'portfinder'
import path from 'path'
import { fileURLToPath } from 'url'

const dir = path.dirname(fileURLToPath(import.meta.url))

app.on('window-all-closed', function () {
    app.quit()
})

app.on('ready', function () {
    portfinder.getPort(function (_err, port) {
        const subpy = spawn('python', ['server.py', dir + '/frontend', port], { cwd: dir + '/backend', stdio: 'inherit' })
        const mainAddr = 'http://localhost:' + port

        const startUp = function () {
            fetch(mainAddr)
                .then(function () {
                    const mainWindow = new BrowserWindow({ width: 800, height: 600 })
                    mainWindow.loadURL(mainAddr)
                    mainWindow.on('closed', function () {
                        subpy.kill('SIGINT')
                    })
                })
                .catch(function () {
                    startUp()
                })
        }

        startUp()
    })
})
