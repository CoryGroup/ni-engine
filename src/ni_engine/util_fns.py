import quantities as pq



def assume_units(value, units):
    """
    If units are not provided for ``value`` (that is, if it is a raw
    `float`), then returns a `~quantities.Quantity` with magnitude
    given by ``value`` and units given by ``units``.
    """
    if not isinstance(value, pq.Quantity):
        value = pq.Quantity(value, units)
    return value

def rescale_with_default(quantity, units):
	quantity = assume_units(quantity, units)
	return quantity.rescale(units).magnitude

