from flask import current_app
from .models import User, Need, Customer, CustomerContact
from elasticsearch_dsl import Search


def get_user_from_email(email, index='rastarockets_users'):
    """
    Return user from unique email address

    :param email: User email address
    :type email: str

    :param index: Index name (optional)
    :type index: str

    :return: User if exist
    :rtype: User|None
    """

    search = Search(
        using=current_app.els_client,
        index=index
    ).query('match_phrase', Email=email)

    response = search.execute()

    if response.hits.total > 0:
        return User(response.hits[0])

    else:
        return None


def get_user_from_id(user_id, index='rastarockets_users'):
    """
    Return user from unique ID

    :param user_id: User unique ID
    :type user_id: str

    :param index: Index name (optional)
    :type index: str

    :return: User if exist
    :rtype: User|None
    """

    search = Search(
        using=current_app.els_client,
        index=index
    ).query('term', _id=user_id)

    response = search.execute()

    if response.hits.total > 0:
        return User(response.hits[0])

    else:
        return None


def get_need_from_id(need_id, index='rastarockets_needs'):
    """
    Return need from unique ID
    
    :param need_id: Need unique ID
    :type need_id: str
    
    :param index: Index name (optional)
    :type index: str
    
    :return: Need if exist
    :rtype: Need|None
    """

    search = Search(
        using=current_app.els_client,
        index=index
    ).query('term', _id=need_id)

    response = search.execute()

    if response.hits.total > 0:
        return Need(response.hits[0])

    else:
        return None


def get_needs(start, size, author_id=None, title=None, status=None, customer_id=None, index='rastarockets_needs'):
    """
    Return list of needs from parameters

    :param start: Start index (pagination)
    :type start: int

    :param size: Number of needs (pagination)
    :type size: int

    :param author_id: Author ID of needs
    :type author_id: str

    :param title: Title of need (optional)
    :type title: str

    :param status: Status of need (optional)
    :type status: str

    :param customer_id: Customer unique ID (optional)
    :type customer_id: str

    :param index: Index name
    :type index: str

    :return: List of needs
    :rtype: list
    """

    needs = []

    search = Search(
        using=current_app.els_client,
        index=index,
        doc_type='need'
    )

    if author_id is not None:
        search = search.query('match_phrase', Author=author_id)

    if title is not None:
        search = search.query('match', Title=title)

    if status is not None:
        search = search.query('match_phrase', Status=status)

    if customer_id is not None:
        search = search.query('match_phrase', Customer=customer_id)

    search = search[start, size]

    response = search.execute()

    for need in response:
        needs.append(Need(need))

    return needs


def add_need_from_parameters(parameters):
    """
    Add need from parameters

    :param parameters: Form parameters
    :type parameters: dict

    :return: Need created
    :rtype: Need|None
    """

    # TODO save need
    return None


def delete_need_from_id(need_id, index='rastarockets_needs'):
    """
    Delete need from unique ID

    :param need_id: Need unique ID
    :type need_id: str

    :param index: Index name (optional)
    :type index: str

    :return: True if success, else False
    :rtype: bool
    """

    response = current_app.els_client.delete_by_query(
        index=index,
        doc_type='need',
        body={
            'query': {
                'term': {'_id': need_id}
            }
        }
    )

    # TODO get response value
    return True


def get_customer_from_id(customer_id, index='rastarockets_customers'):
    """
    Return customer from unique ID

    :param customer_id: Customer unique ID
    :type customer_id: str

    :param index: Index name (optional)
    :type index: str

    :return: Customer if exist
    :rtype: Customer|None
    """
    search = Search(
        using=current_app.els_client,
        index=index,
        doc_type='customer'
    ).query('term', _id=customer_id)

    response = search.execute()

    if response.hits.total > 0:
        return Customer(response.hits[0])

    else:
        return None


def get_possible_customers(prefix, index='rastarockets_customers'):
    """
    Return possible customers from prefix

    :param prefix: Prefix of customer name
    :type prefix: str

    :param index: Index name (optional)
    :type index: str

    :return: List of possible customers
    :rtype: list
    """

    customers = []

    search = Search(
        using=current_app.els_client,
        index=index
    ).query('match', Name=prefix)

    response = search.execute()

    for customer in response:
        customers.append(Customer(customer))

    return customers


def get_contact_from_id(contact_id, index='rastarockets_customers'):
    """
    Return contact from unique ID

    :param contact_id: Contact unique ID
    :type contact_id: str

    :param index: Index name (optional)
    :type index: str

    :return: Contact if exist
    :rtype: Contact|None
    """
    search = Search(
        using=current_app.els_client,
        index=index,
        doc_type='contact'
    ).query('term', _id=contact_id)

    response = search.execute()

    if response.hits.total > 0:
        return CustomerContact(response.hits[0])

    else:
        return None


def get_possible_contacts(prefix, customer=None, index='rastarockets_customers'):
    """
    Return possible contacts from prefix

    :param prefix: Prefix of contact name
    :type prefix: str

    :param customer: Customer ID
    :type customer: str|None

    :param index: Index name (optional)
    :type index: str

    :return: List of possible contacts
    :rtype: list
    """

    contacts = []

    search = Search(
        using=current_app.els_client,
        index=index,
        doc_type='contact'
    ).query('match', Name=prefix)

    if customer is not None:
        search = search.query('match_phrase', Customer=customer)

    response = search.execute()

    for contact in response:
        contacts.append(CustomerContact(contact))

    return contacts


def get_consultant_from_id(consultant_id, index='rastarockets_users'):
    """
    Return consultant from unique ID

    :param consultant_id: Consultant unique ID
    :type consultant_id: str

    :param index: Index name (optional)
    :type index: str

    :return: User if exist
    :rtype: User|None
    """
    search = Search(
        using=current_app.els_client,
        index=index,
        doc_type='user'
    ).query('term', _id=consultant_id).query('match_phrase', Role='consultant')

    response = search.execute()

    if response.hits.total > 0:
        return User(response.hits[0])

    else:
        return None


def get_possible_consultants(prefix, index='rastarockets_users'):
    """
    Return possible consultants from prefix

    :param prefix: Prefix of consultant name
    :type prefix: str

    :param index: Index name (optional)
    :type index: str

    :return: List of possible consultants
    :rtype: list
    """

    consultants = []

    search = Search(
        using=current_app.els_client,
        index=index,
        doc_type='user'
    ).query('match', Name=prefix).query('match_phrase', Role='consultant')

    response = search.execute()

    for consultant in response:
        consultants.append(User(consultant))

    return consultants
