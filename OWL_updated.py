from owlready2 import *

onto = get_ontology("http://example.org/books.owl")

with onto:

    class Book(Thing): pass
    class Person(Thing): pass
    class Series(Thing): pass
    class Audience(Thing): pass
    class Children(Audience): pass
    class Content(Thing): pass
    class MatureContent(Content): pass
    class Friendship(Content): pass
    class Language(Thing): pass
    class LiteraryAward(Thing): pass
    class AwardWin(Thing): pass
    class Fiction(Book): pass
    class NonFiction(Book): pass
    class Fantasy(Fiction): pass



    # Added classes: publishing, formats, audience, works, library
    class Organization(Thing): pass
    class Publisher(Organization): pass
    class ISBN(Thing): pass
    class Hardcover(Book): pass
    class Paperback(Book): pass
    class EBook(Book): pass
    class Audiobook(Book): pass
    class YoungAdult(Audience): pass
    class EducationalContent(Content): pass
    class LiteraryWork(Thing): pass
    class Adaptation(LiteraryWork): pass
    class Library(Organization): pass
    class LibraryCopy(Thing): pass
    class Loan(Thing): pass

    LibraryCopy.is_a.append(Not(Book))

    AllDisjoint([Person, Book])
    AllDisjoint([Series, Book])
    AllDisjoint([Audience, Person])
    AllDisjoint([Content, Book])
    AllDisjoint([LiteraryAward, Book])
    AllDisjoint([Language, Book])
    AllDisjoint([Fiction, NonFiction])
    AllDisjoint([Friendship, MatureContent])
    Book.equivalent_to.append(Fiction | NonFiction)

    class hasAuthor(ObjectProperty):
        domain = [Book]
        range = [Person]
    class isAuthorOf(ObjectProperty):
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


    # Added object properties
    class hasPublisher(ObjectProperty):
        range = [Publisher]
    class hasISBN(ObjectProperty):
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
    class hasSequel(ObjectProperty):
        domain = [Book]
        range = [Book]
    class hasPreviousBook(ObjectProperty):
        domain = [Book]
        range = [Book]
        inverse_property = hasSequel
    class adaptationOf(ObjectProperty):
        range = [LiteraryWork]

    AwardWin.is_a.append(ofAward.some(LiteraryAward))

    dutch = Language("dutch")


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
        equivalent_to = [Book & inLanguage.value(dutch)]   # 具体个体



    # Added defined classes (equivalentClass axioms)
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

    harryPotter = Series("harryPotter")
    hugoAward = LiteraryAward("hugoAward")
    jkRowling = Person("jkRowling")
    dickBruna = Person("dickBruna")

    theHobbit = Fantasy("theHobbit")
    theHobbit.is_a.append(hasTargetAudience.some(Children))

    deHobbit = Book("deHobbit")
    deHobbit.translationOf = [theHobbit]
    deHobbit.inLanguage = [dutch]

    w1 = AwardWin("w1")
    w1.ofAward = [hugoAward]

    hpGobletOfFire = Fantasy("hpGobletOfFire")
    hpGobletOfFire.hasAuthor = [jkRowling]
    hpGobletOfFire.partOfSeries = [harryPotter]
    hpGobletOfFire.received = [w1]

    nijntje = Book("nijntje")
    nijntje.hasAuthor = [dickBruna]
    nijntje.hasIllustrator = [dickBruna]
    nijntje.is_a.append(hasTargetAudience.some(Children))
    nijntje.is_a.append(containsContent.some(Friendship))
    nijntje.is_a.append(containsContent.only(Friendship))


    # Added sample individuals for testing the new definitions
    penguinRandomHouse = Publisher("penguinRandomHouse")
    isbn9780451524935 = ISBN("isbn9780451524935")
    nineteenEightyFour = Fiction("nineteenEightyFour")
    nineteenEightyFour.hasISBN = [isbn9780451524935]

    theHobbitHardcover = Hardcover("theHobbitHardcover")
    theHobbitHardcover.hasPublisher = [penguinRandomHouse]
    theHobbitPaperback = Paperback("theHobbitPaperback")
    theHobbitEbook = EBook("theHobbitEbook")
    theHobbitAudio = Audiobook("theHobbitAudio")

    centralLibrary = Library("centralLibrary")
    hobbitCopy1 = LibraryCopy("hobbitCopy1")
    theHobbit.hasCopy = [hobbitCopy1]
    hobbitCopy1.heldBy = [centralLibrary]
    loan1 = Loan("loan1")
    loan1.loanFor = [hobbitCopy1]

    youngAdultAudience = YoungAdult("youngAdultAudience")
    mathContent = EducationalContent("mathContent")
    mathBook = NonFiction("mathBook")
    mathBook.containsContent = [mathContent]
    mathBook.hasIllustrator = [dickBruna]
    mathBook.hasTargetAudience = [Children("childrenAudience")]
    bookYA = Fiction("bookYA")
    bookYA.hasTargetAudience = [youngAdultAudience]

    hobbitWork = LiteraryWork("hobbitWork")
    hobbitAdaptation = Adaptation("hobbitAdaptation")
    bookAdaptation = Fiction("bookAdaptation")
    bookAdaptation.adaptationOf = [hobbitWork]

    bookA = Fiction("bookA")
    bookB = Fiction("bookB")
    bookA.hasSequel = [bookB]
    # hasPreviousBook(bookB, bookA) follows from the inverse-property axiom.


onto.save(file="books_updated.owl", format="rdfxml")