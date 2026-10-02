@rem Gradle wrapper para Windows con deteccion automatica de JDK.
@rem Prioridad: 1) JAVA_HOME  2) JBR de IntelliJ IDEA  3) JDK de Android Studio  4) java en PATH
@rem (Forge 26.2 pide toolchain Java 25; el JDK de arranque puede ser 17 o superior,
@rem  Gradle descarga el 25 via el foojay-resolver de settings.gradle)
@echo off
setlocal

set "APP_HOME=%~dp0"
set "JAVA_EXE="

rem 1) JAVA_HOME definido
if defined JAVA_HOME (
    if exist "%JAVA_HOME%\bin\java.exe" set "JAVA_EXE=%JAVA_HOME%\bin\java.exe"
)

rem 2) Runtime incluido de IntelliJ IDEA
if not defined JAVA_EXE (
    for /d %%D in ("%ProgramFiles%\JetBrains\*") do (
        if exist "%%D\jbr\bin\java.exe" set "JAVA_EXE=%%D\jbr\bin\java.exe"
    )
)

rem 3) JDK incluido de Android Studio
if not defined JAVA_EXE (
    for /d %%D in ("%ProgramFiles(x86)%\Android\openjdk\jdk-*") do (
        if exist "%%D\bin\java.exe" set "JAVA_EXE=%%D\bin\java.exe"
    )
)

rem 4) java.exe en el PATH
if not defined JAVA_EXE (
    for %%J in (java.exe) do set "JAVA_EXE=%%~$PATH:J"
)

if not defined JAVA_EXE (
    echo ERROR: No se encontro ningun JDK.
    echo Define JAVA_HOME o instala Java 17 o superior.
    exit /b 1
)

"%JAVA_EXE%" -classpath "%APP_HOME%gradle\wrapper\gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain %*
exit /b %ERRORLEVEL%