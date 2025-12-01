echo off
for %%I in (*.py) do (
    echo Uploading %%I...
    ampy --port %1 put %%I
)

