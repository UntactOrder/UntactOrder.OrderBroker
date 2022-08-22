buildscript {
    extra["kotlin_version"] = "1.7.10"
    extra["ktor_version"] = "2.0.3"
    extra["junit_version"] = "5.9.0"
    extra["compose_version"] = "1.3.0-alpha02"
    extra["android_target_sdk_version"] = 33
    extra["android_min_sdk_version"] = 24
    extra["android_build_tool_version"] = "33.0.0"

    repositories {
        gradlePluginPortal()
        mavenCentral()
        google()
    }

    dependencies {
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:${project.extra["kotlin_version"]}")
        classpath("org.jetbrains.kotlin:kotlin-serialization:${project.extra["kotlin_version"]}")
        classpath("com.android.tools.build:gradle:7.3.0-rc01")
    }
}

group = "io.github.untactorder"
version = "1.0"

allprojects {
    repositories {
        mavenCentral()
        mavenLocal()
        google()

        maven {
            setUrl("https://jitpack.io")
            setUrl("https://kotlin.bintray.com/kotlinx")
            setUrl("https://maven.pkg.jetbrains.space/public/p/compose/dev")
            setUrl("https://dl.bintray.com/jetbrains/kotlin-native-dependencies")

            // Adding Kakao SDK Repo
            setUrl("https://devrepo.kakao.com/nexus/content/groups/public/")
        }
    }
}

tasks.register("clean", Delete::class) {
    delete(rootProject.buildDir)
}
