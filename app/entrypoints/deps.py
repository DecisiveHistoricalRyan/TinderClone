from app.service_layer.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork


def get_uow() -> AbstractUnitOfWork:
    uow = SqlAlchemyUnitOfWork()
    return uow
