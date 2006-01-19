import gtk
import gobject
from gettext import gettext as _
from logging import getLogger

log = getLogger(".ObjectSelector")

from GrampsWidgets import IntEdit
from _FilterFrameBase import FilterFrameBase
import GenericFilter
import RelLib

class PersonFilterFrame(FilterFrameBase):
    
    __gproperties__ = {}

    __gsignals__ = {
        }

    __default_border_width = 5

    def __init__(self,dbstate,label="Filter"):
	FilterFrameBase.__init__(self,label)

        # Gramps ID
        self._id_check = gtk.CheckButton()
        id_label = gtk.Label("Gramps ID")
        id_label.set_alignment(xalign=0,yalign=0.5)

        self._id_edit = gtk.Entry()
        self._id_edit.set_sensitive(False)

        self._id_check.connect('toggled',lambda b: self._id_edit.set_sensitive(self._id_check.get_active()))

        # Name
	self._name_check = gtk.CheckButton()
        name_label = gtk.Label("Name")
        name_label.set_alignment(xalign=0,yalign=0.5)

        self._name_edit = gtk.Entry()
        self._name_edit.set_sensitive(False)
        
        self._name_check.connect('toggled',lambda b: self._name_edit.set_sensitive(self._name_check.get_active()))

        # Gender
	self._gender_check = gtk.CheckButton()
        gender_label = gtk.Label("Gender")
        gender_label.set_alignment(xalign=0,yalign=0.5)

        self._gender_list = gtk.ListStore(str,int)

        genders=[[_("Male"),RelLib.Person.MALE],
                 [_("Female"),RelLib.Person.FEMALE],
                 [_("Unknown"),RelLib.Person.UNKNOWN]]
        
        for gender in genders:        
            self._gender_list.append(gender)
        
        self._gender_combo = gtk.ComboBox(self._gender_list)
        
        label_cell = gtk.CellRendererText()
        
        self._gender_combo.pack_start(label_cell, True)
        self._gender_combo.add_attribute(label_cell, 'text', 0)
        self._gender_combo.set_active(2)
        self._gender_combo.set_sensitive(False)

        self._gender_check.connect('toggled',lambda b: self._gender_combo.set_sensitive(self._gender_check.get_active()))

        # Birth
        self._birth_check = gtk.CheckButton()
        self._birth_check.set_alignment(xalign=0,yalign=0)

        b_label = gtk.Label("Birth Year")
        b_label.set_alignment(xalign=0,yalign=0)
        
        self._b_edit = IntEdit()
        self._b_edit.set_sensitive(False)

        self._b_before = gtk.RadioButton(group=None,label="Before")
        self._b_before.set_sensitive(False)

        self._b_after = gtk.RadioButton(self._b_before,"After")
        self._b_after.set_sensitive(False)
        self._b_before.set_active(True)
        
        self._b_unknown = gtk.CheckButton("Include Unknown")
        self._b_unknown.set_sensitive(False)
        self._b_unknown.set_active(True)

        self._birth_check.connect('toggled',lambda b: self._b_edit.set_sensitive(self._birth_check.get_active()))
        self._birth_check.connect('toggled',lambda b: self._b_before.set_sensitive(self._birth_check.get_active()))
        self._birth_check.connect('toggled',lambda b: self._b_after.set_sensitive(self._birth_check.get_active()))
        self._birth_check.connect('toggled',lambda b: self._b_unknown.set_sensitive(self._birth_check.get_active()))

        self._b_inner_box = gtk.HBox()
        self._b_inner_box.pack_start(self._b_before)
        self._b_inner_box.pack_start(self._b_after)
        
        # Death

        self._death_check = gtk.CheckButton()

        d_label = gtk.Label("Death Year")
        d_label.set_alignment(xalign=0,yalign=0)

        self._d_edit = IntEdit()
        self._d_edit.set_sensitive(False)

        self._d_before = gtk.RadioButton(group=None,label="Before")
        self._d_before.set_sensitive(False)

        self._d_after = gtk.RadioButton(self._d_before,"After")
        self._d_after.set_sensitive(False)

        self._d_before.set_active(True)
        self._d_before.set_sensitive(False)

        self._d_unknown = gtk.CheckButton("Include Unknown")
        self._d_unknown.set_sensitive(False)
        self._d_unknown.set_active(True)

        self._death_check.connect('toggled',lambda b: self._d_edit.set_sensitive(self._death_check.get_active()))
        self._death_check.connect('toggled',lambda b: self._d_before.set_sensitive(self._death_check.get_active()))
        self._death_check.connect('toggled',lambda b: self._d_after.set_sensitive(self._death_check.get_active()))
        self._death_check.connect('toggled',lambda b: self._d_unknown.set_sensitive(self._death_check.get_active()))

        d_inner_box = gtk.HBox()
        d_inner_box.pack_start(self._d_before)
        d_inner_box.pack_start(self._d_after)

        # Filter
	self._filter_check = gtk.CheckButton()
        filter_label = gtk.Label("Filter")
        filter_label.set_alignment(xalign=0,yalign=0.5)

        default_filters = [
            GenericFilter.Everyone,
            GenericFilter.IsFemale,
            GenericFilter.IsMale,
            GenericFilter.HasUnknownGender,
            GenericFilter.Disconnected,
            GenericFilter.SearchName,
            GenericFilter.HaveAltFamilies,
            GenericFilter.HavePhotos,
            GenericFilter.IncompleteNames,
            GenericFilter.HaveChildren,
            GenericFilter.NeverMarried,
            GenericFilter.MultipleMarriages,
            GenericFilter.NoBirthdate,
            GenericFilter.PersonWithIncompleteEvent,
            GenericFilter.FamilyWithIncompleteEvent,
            GenericFilter.ProbablyAlive,
            GenericFilter.PeoplePrivate,
            GenericFilter.IsWitness, 
            GenericFilter.HasTextMatchingSubstringOf, 
            GenericFilter.HasTextMatchingRegexpOf, 
            GenericFilter.HasNote, 
            GenericFilter.HasNoteMatchingSubstringOf, 
            GenericFilter.IsFemale,
            ]

        self._filter_list = gtk.ListStore(object,str)

        for filter in default_filters:
            if not hasattr(filter,'labels') or len(filter.labels) == 0:
                # don't currently support filters that need an attribute.
                self._filter_list.append([filter,filter.name])
        
        self._filter_combo = gtk.ComboBox(self._filter_list)
        
        label_cell = gtk.CellRendererText()
        
        self._filter_combo.pack_start(label_cell, True)
        self._filter_combo.add_attribute(label_cell, 'text', 1)
        self._filter_combo.set_active(0)
        self._filter_combo.set_sensitive(False)

        self._filter_check.connect('toggled',lambda b: self._filter_combo.set_sensitive(self._filter_check.get_active()))

        self._filter_entry_label = gtk.Label()
        self._filter_entry_label.set_sensitive(False)
        
        self._filter_entry_edit = gtk.Entry()
        self._filter_entry_edit.set_sensitive(False)
        
        # table layout
        
        current_row = 0
        
        self._table.attach(self._id_check,self._check_col,self._check_col+1,
                           current_row,current_row+1,xoptions=False,yoptions=False)
        self._table.attach(id_label,self._label_col,self._label_col+1,
                           current_row,current_row+1,xoptions=gtk.FILL,yoptions=False)
        self._table.attach(self._id_edit,self._control_col,self._control_col+1,
                           current_row,current_row+1,xoptions=gtk.EXPAND|gtk.FILL,yoptions=False)

        current_row +=1
        
        self._table.attach(self._name_check,self._check_col,self._check_col+1,
                           current_row,current_row+1,xoptions=False,yoptions=False)
        self._table.attach(name_label,self._label_col,self._label_col+1,
                           current_row,current_row+1,xoptions=gtk.FILL,yoptions=False)
        self._table.attach(self._name_edit,self._control_col,self._control_col+1,
                           current_row,current_row+1,xoptions=gtk.EXPAND|gtk.FILL,yoptions=False)

        current_row +=1

        self._table.attach(self._gender_check,self._check_col,self._check_col+1,
                           current_row,current_row+1,xoptions=False,yoptions=False)
        self._table.attach(gender_label,self._label_col,self._label_col+1,
                           current_row,current_row+1,xoptions=gtk.FILL,yoptions=False)
        self._table.attach(self._gender_combo,self._control_col,self._control_col+1,
                           current_row,current_row+1,xoptions=gtk.EXPAND|gtk.FILL,yoptions=False)


        current_row +=1

        self._table.attach(self._birth_check,self._check_col,self._check_col+1,
                           current_row,current_row+1,xoptions=False,yoptions=False)
        self._table.attach(b_label,self._label_col,self._label_col+1,
                           current_row,current_row+1,xoptions=gtk.FILL,yoptions=False)
        self._table.attach(self._b_edit,self._control_col,self._control_col+1,
                           current_row,current_row+1,xoptions=gtk.EXPAND|gtk.FILL,yoptions=False)
        
        current_row +=1
        self._table.attach(self._b_inner_box,self._control_col,self._control_col+1,
                           current_row,current_row+1,xoptions=gtk.EXPAND|gtk.FILL,yoptions=False)
        
        current_row +=1
        self._table.attach(self._b_unknown,self._control_col,self._control_col+1,
                           current_row,current_row+1,xoptions=gtk.EXPAND|gtk.FILL,yoptions=False)

        current_row +=1

        self._table.attach(self._death_check,self._check_col,self._check_col+1,
                           current_row,current_row+1,xoptions=False,yoptions=False)
        self._table.attach(d_label,self._label_col,self._label_col+1,current_row,
                           current_row+1,xoptions=gtk.FILL,yoptions=False)
        self._table.attach(self._d_edit,self._control_col,self._control_col+1,
                           current_row,current_row+1,xoptions=gtk.EXPAND|gtk.FILL,yoptions=False)
        
        current_row +=1
        self._table.attach(d_inner_box,self._control_col,self._control_col+1,
                           current_row,current_row+1,xoptions=gtk.EXPAND|gtk.FILL,yoptions=False)
        
        current_row +=1
        self._table.attach(self._d_unknown,self._control_col,self._control_col+1,
                           current_row,current_row+1,xoptions=gtk.EXPAND|gtk.FILL,yoptions=False)

        current_row +=1

        self._table.attach(self._filter_check,self._check_col,self._check_col+1,
                           current_row,current_row+1,xoptions=False,yoptions=False)
        self._table.attach(filter_label,self._label_col,self._label_col+1,
                           current_row,current_row+1,xoptions=gtk.FILL,yoptions=False)
        self._table.attach(self._filter_combo,self._control_col,self._control_col+1,
                           current_row,current_row+1,xoptions=gtk.EXPAND|gtk.FILL,yoptions=False)

    def on_apply(self,button):
        filter = GenericFilter.GenericFilter()
        
        if self._id_check.get_active():
            filter.add_rule(GenericFilter.HasIdOf([self._id_edit.get_text()]))

        if self._name_check.get_active():
            filter.add_rule(GenericFilter.SearchName([self._name_edit.get_text()]))

        if self._gender_check.get_active():
            gender = self._gender_list.get_value(self._gender_combo.get_active_iter(),1)
            if gender == RelLib.Person.MALE:
                filter.add_rule(GenericFilter.IsMale([]))
            elif gender == RelLib.Person.FEMALE:
                filter.add_rule(GenericFilter.IsFemale([]))
            elif gender == RelLib.Person.UNKNOWN:
                filter.add_rule(GenericFilter.HasUnknownGender([]))
            else:
                log.warn("Received unknown gender from filter widget")

        if self._birth_check.get_active():
            date = ""
            if self._b_before.get_active():
                date = "before " + self._b_edit.get_text()
            elif self._b_after.get_active():
                date = "after " + self._b_edit.get_text()
            else:
                log.warn("neither before or after is selected, this should not happen")
            filter.add_rule(GenericFilter.HasBirth([date,'','']))
                
        if self._death_check.get_active():
            date = ""
            if self._d_before.get_active():
                date = "before " + self._d_edit.get_text()
            elif self._d_after.get_active():
                date = "after " + self._d_edit.get_text()
            else:
                log.warn("neither before or after is selected, this should not happen")
            filter.add_rule(GenericFilter.HasDeath([date,'','']))


        if self._filter_check.get_active():
            filter.add_rule(self._filter_list.get_value(self._filter_combo.get_active_iter(),0)([]))

            
	self.emit('apply-filter',filter)
    
if gtk.pygtk_version < (2,8,0):
    gobject.type_register(PersonFilterFrame)

if __name__ == "__main__":

    w = gtk.Window()
    f = PersonFilterFrame()
    w.add(f)
    
    w.show_all()

    gtk.main()
