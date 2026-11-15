
from owlready2 import (
    AllDisjoint,
    FunctionalProperty,
    InverseFunctionalProperty,
    Not,
    ObjectProperty,
    Thing,
    TransitiveProperty,
    get_ontology,
)

onto = get_ontology("http://example.org/books.owl")

with onto:
    # ------------------------------------------------------------------
    # Classes (28)
    # ------------------------------------------------------------------
    class Book(Thing): pass                  # one concrete edition of a book
    class Fiction(Book): pass
    class NonFiction(Book): pass
    class Fantasy(Fiction): pass
    class Hardcover(Book): pass
    class Paperback(Book): pass
    class EBook(Book): pass
    class Audiobook(Book): pass
    class Series(Thing): pass
    class Person(Thing): pass
    class Audience(Thing): pass
    class Children(Audience): pass
    class YoungAdult(Audience): pass
    class Content(Thing): pass
    class MatureContent(Content): pass
    class Friendship(Content): pass
    class EducationalContent(Content): pass
    class LiteraryAward(Thing): pass
    class AwardWin(Thing): pass              # reifies wonAward(book, award)
    class Language(Thing): pass
    class Organization(Thing): pass
    class Publisher(Organization): pass
    class Library(Organization): pass
    class ISBN(Thing): pass
    class LiteraryWork(Thing): pass          # abstract work, independent of editions
    class Adaptation(LiteraryWork): pass
    class LibraryCopy(Thing): pass
    class Loan(Thing): pass

    # Book ≡ Fiction ⊔ NonFiction  (covering axiom)
    Book.equivalent_to.append(Fiction | NonFiction)

    # Disjointness axioms
    AllDisjoint([Fiction, NonFiction])       # Fiction ⊑ ¬NonFiction
    AllDisjoint([Series, Book])
    AllDisjoint([Person, Book])
    AllDisjoint([Audience, Person])
    AllDisjoint([Content, Book])
    AllDisjoint([Friendship, MatureContent]) # Friendship ⊑ ¬MatureContent
    AllDisjoint([LiteraryAward, Book])
    AllDisjoint([Language, Book])
    AllDisjoint([LibraryCopy, Book])         # LibraryCopy ⊑ ¬Book

    # ------------------------------------------------------------------
    # Roles (19)
    # ------------------------------------------------------------------
    class hasAuthor(ObjectProperty):         # ∃hasAuthor.⊤ ⊑ Book; ⊤ ⊑ ∀hasAuthor.Person
        domain = [Book]
        range = [Person]

    class isAuthorOf(ObjectProperty):        # isAuthorOf ≡ hasAuthor⁻  (inverse role)
        inverse_property = hasAuthor

    class hasIllustrator(ObjectProperty):
        domain = [Book]
        range = [Person]

    class hasTargetAudience(ObjectProperty):
        range = [Audience]

    class containsContent(ObjectProperty):
        range = [Content]

    class partOfSeries(ObjectProperty):
        range = [Series]

    class translationOf(ObjectProperty):
        range = [Book]

    class inLanguage(ObjectProperty):
        range = [Language]

    class received(ObjectProperty):
        range = [AwardWin]

    class ofAward(ObjectProperty):
        range = [LiteraryAward]

    class hasPublisher(ObjectProperty):
        range = [Publisher]

    # Func(hasISBN); InvFunc(hasISBN)  (functional and inverse functional role)
    class hasISBN(ObjectProperty, FunctionalProperty, InverseFunctionalProperty):
        range = [ISBN]

    class hasCopy(ObjectProperty):
        domain = [Book]
        range = [LibraryCopy]

    class heldBy(ObjectProperty):
        domain = [LibraryCopy]
        range = [Library]

    class loanFor(ObjectProperty):
        domain = [Loan]
        range = [LibraryCopy]

    class adaptationOf(ObjectProperty):
        range = [LiteraryWork]

    class precedes(ObjectProperty, TransitiveProperty):  # Trans(precedes)  (transitive role)
        pass

    class hasSequel(precedes):               # hasSequel ⊑ precedes  (role hierarchy)
        range = [Book]

    class hasPreviousBook(ObjectProperty):   # hasSequel ≡ hasPreviousBook⁻
        range = [Book]
        inverse_property = hasSequel

    # Class axioms that use roles
    AwardWin.is_a.append(ofAward.some(LiteraryAward))

    # Needed before DutchBook, which uses the nominal {dutch}
    dutch = Language("dutch")

    # ------------------------------------------------------------------
    # Defined classes (18)
    # ------------------------------------------------------------------
    class Author(Thing):
        equivalent_to = [Person & isAuthorOf.some(Book)]

    class TranslatedBook(Thing):
        equivalent_to = [Book & translationOf.some(Book)]

    class SeriesBook(Thing):
        equivalent_to = [Book & partOfSeries.some(Thing)]

    class IllustratedBook(Thing):
        equivalent_to = [Book & hasIllustrator.some(Person)]

    class PictureBook(Thing):
        equivalent_to = [IllustratedBook & hasTargetAudience.some(Children)]

    class ChildrensFantasyBook(Thing):
        equivalent_to = [Fantasy & hasTargetAudience.some(Children)]

    class ChildFriendlyBook(Thing):
        equivalent_to = [Book & containsContent.only(Not(MatureContent))]

    class PrizeWinningBook(Thing):
        equivalent_to = [Book & received.some(AwardWin & ofAward.some(LiteraryAward))]

    class AwardWinningAuthor(Thing):
        equivalent_to = [Author & isAuthorOf.some(PrizeWinningBook)]

    class DutchBook(Thing):
        equivalent_to = [Book & inLanguage.value(dutch)]     # nominal

    class PublishedBook(Thing):
        equivalent_to = [Book & hasPublisher.some(Publisher)]

    class EducationalBook(Thing):
        equivalent_to = [Book & containsContent.some(EducationalContent)]

    class YoungAdultBook(Thing):
        equivalent_to = [Book & hasTargetAudience.some(YoungAdult)]

    class IllustratedEducationalBook(Thing):
        equivalent_to = [EducationalBook & IllustratedBook]

    class ChildrensEducationalBook(Thing):
        equivalent_to = [EducationalBook & hasTargetAudience.some(Children)]

    class SequelBook(Thing):
        equivalent_to = [Book & hasPreviousBook.some(Book)]

    class BookWithSequel(Thing):
        equivalent_to = [Book & hasSequel.some(Book)]

    class AdaptedBook(Thing):
        equivalent_to = [Book & adaptationOf.some(LiteraryWork)]

    # ------------------------------------------------------------------
    # Individuals (10; dutch is created above)
    # ------------------------------------------------------------------
    theHobbit = Fantasy("theHobbit")
    theHobbit.is_a.append(hasTargetAudience.some(Children))

    deHobbit = Book("deHobbit", translationOf=[theHobbit], inLanguage=[dutch])

    harryPotter = Series("harryPotter")
    hugoAward = LiteraryAward("hugoAward")
    w1 = AwardWin("w1", ofAward=[hugoAward])
    jkRowling = Person("jkRowling")
    hpGobletOfFire = Fantasy("hpGobletOfFire", hasAuthor=[jkRowling],
                             partOfSeries=[harryPotter], received=[w1])

    dickBruna = Person("dickBruna")
    nijntje = Book("nijntje", hasAuthor=[dickBruna], hasIllustrator=[dickBruna])
    nijntje.is_a.append(hasTargetAudience.some(Children))
    nijntje.is_a.append(containsContent.some(Friendship))
    nijntje.is_a.append(containsContent.only(Friendship))  # closure axiom


if __name__ == "__main__":
    onto.save(file="books.owl", format="rdfxml")
    print("Saved books.owl")