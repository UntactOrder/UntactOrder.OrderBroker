import io.github.untactorder.orderbroker.App
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application

fun main() = application {
    Window(
        onCloseRequest = ::exitApplication,
        undecorated = false
    ) {
        App()
    }
}
