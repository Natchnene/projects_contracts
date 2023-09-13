from sqlite import db
from services import (create_contract, sign_contract, finalise_contract, create_project, add_contract, finalise_contract_from_project)


def main():
    while True:
        print("\n1. Договор\n2. Проект\n3. Список проектов\n4. Список договоров\n5. Завершить работу с программой\n")
        option = input("Выберите действие: ")

        if option == "1":
            print("\n1. Создать договор\n2. Подтвердить договор\n3. Завершить договор\n")
            contract_option = input("Выберите действие: ")
            if contract_option == "1":
                print(create_contract())
            elif contract_option == "2":
                sign_contract()
            elif contract_option == "3":
                finalise_contract()

        elif option == "2":
            print("\n1. Создать проект\n2. Добавить договор\n3. Завершить договор\n")
            project_option = input("Выберите действие: ")
            if project_option == "1":
                create_project()
            elif project_option == "2":
                add_contract()
            elif project_option == "3":
                finalise_contract_from_project()

        elif option == "3":
            db.all_projects()

        elif option == "4":
            db.all_contracts()

        elif option == "5":
            db.connection.close()
            print("\nПрограмма успешно завершена.")
            break

        else:
            print("Неверное действие.")


main()
