from printerIO.models import PrintingModel
from typing import Iterable


def get_models() -> Iterable[PrintingModel]:
    return PrintingModel.objects.all()


def get_model(model_id: int) -> PrintingModel:
    return PrintingModel.objects.get(pk=model_id)
