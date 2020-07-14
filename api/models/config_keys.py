from pydantic import BaseModel, Field
from typing import Optional
from humps import decamelize

def to_snake(string):
    return decamelize(string)


class SnakeModel(BaseModel):
  class Config:
      alias_generator = to_snake
      allow_population_by_field_name = True


class AppConfig(SnakeModel):
    VideoPath: Optional[str] = Field(None, example='/repo/data/TownCentreXVID.avi')
    Resolution: Optional[str] = Field(None, example='640,480')
    Encoder: Optional[str] = Field(None, example='videoconvert ! video/x-raw,format=I420 ! x264enc speed-preset=ultrafast')


class Config(SnakeModel):
    App: Optional[AppConfig]


class ConfigRequest(BaseModel):
    save_file: Optional[bool] = Field(False)
    config: Config
