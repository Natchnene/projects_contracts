from sqlite import db
from models import Project, Contract


def create_contract():
    name = input("\nВведите название договора: ")
    contract = Contract(name)
    contract.save()
    return f"\nДоговор '{name}' успешно создан."


def sign_contract():
    """ You can sign only "draft" contract """
    draft_contracts = db.all_draft_contracts()
    if len(draft_contracts) != 0:
        print("\nСписок договоров:")
        for contract in draft_contracts:
            print(f"ID-{contract[0]} {contract[1]} {contract[4]}")
        contract_id = input("\nВведите ID договора для его подтверждения: ")
        return db.sign(contract_id)
    else:
        print("\nУ вас нет договоров в статусе 'Черновик'.")


def finalise_contract():
    """ You can finalize only active contract """
    active_contracts = db.all_active_contracts()
    if len(active_contracts) != 0:
        print("\nСписок договоров:")
        for contract in active_contracts:
            print(f"ID-{contract[0]} {contract[1]} {contract[4]} Дата подписания: {contract[2]}")
        contract_id = input("\nВведите ID договора для его завершения: ")
        return db.finalise(contract_id)
    else:
        return "У вас нет договоров в статусе 'Активен'."


def create_project():
    """ You can create project only if you have active and free contract """
    active_free_contracts = db.all_active_free_contracts()
    if len(active_free_contracts) != 0:
        name = input("\nВведите название проекта: ")
        project = Project(name)
        project.save()
        print(f"\nПроект '{name}' успешно создан.")
    else:
        print("\nВы не можете создать проект, так как у вас нет активных договоров.")


def add_contract():
    active_free_contracts = db.all_active_free_contracts()
    if len(active_free_contracts) != 0:
        print("\nСписок договоров:")
        for contract in active_free_contracts:
            print(f"ID-{contract[0]} {contract[1]} {contract[4]} Дата подписания: {contract[2]}")
        contract_id = input("\nВведите ID договора: ")
        db.all_projects()
        project_id = input("\nВведите ID проекта: ")
        return db.add_contract(project_id, contract_id)
    else:
        return "\nУ вас нет новых договоров."


def finalise_contract_from_project():
    """ You can finalize only active contract, which has project. """
    all_active_projects = db.all_active_projects()
    if len(all_active_projects) != 0:
        print("\nСписок проектов:")
        for project_contract in all_active_projects:
            print(f"ПРОЕКТ: ID-{project_contract[0]} {project_contract[1]} "
                  f"ДОГОВОР: ID-{project_contract[3]} {project_contract[4]} "
                  f"Дата подписания - {project_contract[6]} Статус - {project_contract[7]}")
        contract_id = input("\nВведите ID договора для его завершения: ")
        return db.finalise(contract_id)
    else:
        return "\nУ вас нет проектов в работе с договорами в статусе 'Активен'."
