import org.jetbrains.compose.compose

plugins {
    kotlin("multiplatform")
    id("org.jetbrains.compose")
    id("com.android.library")
}

kotlin {
    android()

    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach {
        it.binaries.framework {
            baseName = "common"
        }
    }

    jvm("desktop") {
        compilations.all {
            kotlinOptions.jvmTarget = "11"
        }
    }

    sourceSets {
        val commonMain by getting {
            dependencies {
                api(compose.foundation)
                @OptIn(org.jetbrains.compose.ExperimentalComposeLibrary::class) api(compose.material3)
            }
        }
        val commonTest by getting {
            dependencies {
                implementation(kotlin("test"))
            }
        }
        val androidMain by getting {
            dependencies {
                api(compose.ui)
                api(compose.runtime)
                implementation("androidx.compose.ui:ui-tooling-preview:${rootProject.extra["compose_ext_version"]}")
                api("androidx.appcompat:appcompat:1.5.0")
                api("androidx.core:core-ktx:1.8.0")
            }
        }
        val androidTest by getting {
            dependencies {
                implementation("androidx.test.ext:junit-ktx:1.1.3")
                implementation("junit:junit:4.13.2")
            }
        }
        val iosX64Main by getting
        val iosArm64Main by getting
        val iosSimulatorArm64Main by getting
        val iosMain by creating {
            dependsOn(commonMain)
            iosX64Main.dependsOn(this)
            iosArm64Main.dependsOn(this)
            iosSimulatorArm64Main.dependsOn(this)
        }
        val iosX64Test by getting
        val iosArm64Test by getting
        val iosSimulatorArm64Test by getting
        val iosTest by creating {
            dependsOn(commonTest)
            iosX64Test.dependsOn(this)
            iosArm64Test.dependsOn(this)
            iosSimulatorArm64Test.dependsOn(this)
        }
        val desktopMain by getting {
            dependencies {
                api(compose.ui)
                api(compose.runtime)
                api(compose.preview)
            }
        }
        val desktopTest by getting
    }
}

android {
    compileSdk = rootProject.extra["android_target_sdk_version"] as Int?
    buildToolsVersion = rootProject.extra["android_build_tool_version"] as String
    sourceSets["main"].manifest.srcFile("src/androidMain/AndroidManifest.xml")
    defaultConfig {
        minSdk = rootProject.extra["android_min_sdk_version"] as Int?
        targetSdk = rootProject.extra["android_target_sdk_version"] as Int?
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
}
