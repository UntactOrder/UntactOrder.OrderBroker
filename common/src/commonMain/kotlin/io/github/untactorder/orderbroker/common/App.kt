package io.github.untactorder.orderbroker.common

import androidx.compose.material3.Text
import androidx.compose.material3.Button
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import io.github.untactorder.shared.ui.theme.UntactOrderApplicationTheme

@Composable
fun App() {
    UntactOrderApplicationTheme {
        var text by remember { mutableStateOf("Hello, World!") }

        Button(modifier = Modifier, onClick = {
            text = "Hello, ${getPlatformName()}"
        }) {
            Text(text)
        }
        ItemContainer()
    }
}
