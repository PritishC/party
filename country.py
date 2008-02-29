from trytond.osv import fields, OSV
STATES = {
    'readonly': "active == False",
}


class Country(OSV):
    'Country'
    _name = 'partner.country'
    _description = __doc__
    _order='code'
    name = fields.Char('Country Name', size=64,
           help='The full name of the country.', required=True, translate=True)
    code = fields.Char('Country Code', size=2,
           help='The ISO country code in two chars.\n'
           'You can use this field for quick search.', required=True)
    state = fields.One2Many('partner.country.state', 'country', 'State')
    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         'The name of the country must be unique !'),
        ('code_uniq', 'unique (code)',
         'The code of the country must be unique !')
    ]

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=80):
        if not args:
            args=[]
        if not context:
            context={}
        ids = False
        if len(name) <= 2:
            ids = self.search(cr, user, [('code', '=', name)] + args,
                    limit=limit, context=context)
        if not ids:
            ids = self.search(cr, user, [('name', operator, name)] + args,
                    limit=limit, context=context)
        return self.name_get(cr, user, ids, context)

    def create(self, cursor, user, vals, context=None):
        if 'code' in vals:
            vals['code'] = vals['code'].upper()
        return super(Country, self).create(cursor, user, vals, context=context)

    def write(self, cursor, user, ids, vals, context=None):
        if 'code' in vals:
            vals['code'] = vals['code'].upper()
        return super(Country, self).write(cursor, user, ids, vals,
                context=context)

Country()


class State(OSV):
    "State"
    _name = 'partner.country.state'
    _description = __doc__
    _order = 'code'
    country = fields.Many2One('partner.country', 'Country',
            required=True)
    name = fields.Char('State Name', size=64, required=True)
    code = fields.Char('State Code', size=3, required=True)

    def create(self, cursor, user, vals, context=None):
        if 'code' in vals:
            vals['code'] = vals['code'].upper()
        return super(State, self).create(cursor, user, vals,
                context=context)

    def write(self, cursor, user, ids, vals, context=None):
        if 'code' in vals:
            vals['code'] = vals['code'].upper()
        return super(State, self).write(cursor, user, ids, vals,
                context=context)

State()
