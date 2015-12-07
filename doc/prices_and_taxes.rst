Prices and Taxes in Shoop
=========================

This document gives an overview of Shoop's pricing and taxing mechanics.
For deeper view about the implementation -- if you're implementing a
price/tax related addon for example -- read also the
:doc:`prices_and_taxes_implementation` document.

.. _price-unit:

Price Unit
----------

Prices in Shoop have an unit that is combination of a currency and
includes/excludes taxes info.  I.e. prices may be specified pretax or
with taxes included.  Which taxing type and currency is used is usually
decided by the `~shoop.core.models.Shop`.  It has `currency` and
`prices_include_tax` fields.  In general, it is also possible, that the
current `~shoop.core.pricing.PricingModule` uses a different price unit
that is specified by shop, but currently there is no such pricing module
in Shoop Base distribution.

Different price units cannot be mixed: Adding a pretax price and price
including taxes together would make no sense, nor adding USDs to EURs.

Price unit of a `~shoop.core.models.Shop` can be changed as long as
there is no `Orders <shoop.core.models.Order>` created for the shop.

Price unit of `~shoop.core.models.Order` is stored to its ``currency``
and ``prices_include_tax`` fields.  Line prices of order are stored in
that unit, but total price of order is stored with and without taxes
into ``taxful_price`` and ``taxless_price`` fields.

Calculation of Taxes
--------------------

How Taxes Are Determined
~~~~~~~~~~~~~~~~~~~~~~~~

Taxing in Shoop is implemented by a `tax module
<shoop.core.taxing.TaxModule>`.  Shoop Base distribution ships a tax
module called :ref:`Default Tax <default-tax-module>`, but it is
possible to plug in another tax module via :doc:`addons <addons>` or to
implement a new one.

Responsibilities of a tax module are to calculate taxes for an order or
for a separate item (e.g. product, shipping or some other taxable item).
Most important function of a tax module is to take an order source, like
a basket, which has lines (with pretax prices or tax included prices)
and fill in taxes for each line in the source.

When Taxes Are Determined
~~~~~~~~~~~~~~~~~~~~~~~~~

Shoop calculates taxes for a basket in the confirm phase of checkout
process or in the confirm phase of order creating UI in the Shop Admin.
This means that taxes are not known for items in the basket, product
listings or in a detail page of a product.  Reason for not calculating
taxes before the confirm phase, is that the used tax module might query
the taxes from an external source which might be slow or cost a
transaction fee.

.. TODO:: Update this documentation after SHOOP-1911 (Automatically
          calculating taxes if cheap) is implemented.

Taxes in Orders
---------------

Taxes are stored to order lines.  Each order line can have several taxes
applied and each of them is stored to a separate `line tax
<shoop.core.models.OrderLineTax>` object linked to the order line.
Those line tax objects store link to the `~shoop.core.models.Tax`
object, tax name, applied amount and base amount.

.. _default-tax-module:

The Default Tax Module
----------------------

Shoop Default Tax is a tax module that calculates taxes based on a set
of rules which are stored to the database.  Tax rule applies a tax for
order line or any other taxable item (e.g. product or shipping method).
An item could be taxed with several taxes, which will be added together
or compounded over each other.

.. _defining-default-tax-rules:

Defining Tax Rules for The Default Tax Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tax rules of Default Tax can be managed in the Shoop Shop Admin from
*Menu* → *Taxes* → *Tax Rules*.

Most fields of the tax rule determine conditions when the rule applies.
All non-empty fields must match for the rule to apply.  Empty fields are
not considered, e.g. if "Customer tax groups" is left empty, all
customer tax groups will match.  You may use these conditions to apply
certain tax rule only for a specific country or area for example.

Area specific matching criteria fields are specified with a pattern that
is able to match multiple values.  See the help text on the Admin view
for details on how to write those patterns.

If all conditions of a tax rule match, the rule will be applied.  That
means that the tax specified in the rule will be added for the item.  If
there are several rules to be applied for an item, the total tax is
determined by the priority field.  Rules with same priority define added
taxes (e.g. US taxes) and rules with different priority define compound
taxes (e.g. Canada Quebec PST case).

Tax rule may also define an override group number.  If several rules
match, only the rules with the highest override group number will be
effective.  This can be used, for example, to implement tax exemption by
adding a rule with very high override group number that sets a zero tax.
