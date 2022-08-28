plugins {
    id("org.jetbrains.compose")
    id("com.android.application")
    kotlin("android")
}

repositories {
}

dependencies {
    implementation(project(":common"))
    implementation(project(":shared"))
    api("androidx.activity:activity-compose:1.5.1")
}

android {
    namespace = rootProject.extra["organization"] as String? + ".orderbroker"
    compileSdk = rootProject.extra["android_target_sdk_version"] as Int?
    buildToolsVersion = rootProject.extra["android_build_tool_version"] as String
    testOptions {
        unitTests.apply {
            isReturnDefaultValues = true
        }
    }
    defaultConfig {
        applicationId = rootProject.extra["organization"] as String? + ".orderbroker"
        minSdk = rootProject.extra["android_min_sdk_version"] as Int?
        targetSdk = rootProject.extra["android_target_sdk_version"] as Int?
        versionCode = 1
        versionName = rootProject.extra["version"] as String?

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables.useSupportLibrary = true
    }
    sourceSets {
        getByName("main") {
            manifest.srcFile("src/main/AndroidManifest.xml")
            kotlin.srcDirs("src/main/kotlin")
            res.srcDirs("src/main/res")
        }
    }
    buildTypes {
        getByName("release") {
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = "1.8"
    }
    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = rootProject.extra["compose_ext_version"] as String
    }
    packagingOptions {
        resources.excludes += "/META-INF/{AL2.0,LGPL2.1}"
    }
}
