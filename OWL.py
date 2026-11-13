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


onto.save(file="books.owl", format="rdfxml")