import connect from 'connect'
import serveStatic from 'serve-static'

connect()
    .use(serveStatic("./"))
    .listen(8080, () => console.log('Server running on 8080...'))
