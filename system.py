import esper
from typing import Any as _Any
from typing import List as _List
from typing import Type as _Type
from typing import Optional as _Optional

###################
#   ECS Classes
###################

class System:
    """Base class for all Processors to inherit from.

    Processor instances must contain a `process` method, but you are otherwise
    free to define the class any way you wish. Processors should be instantiated,
    and then added to the current World context by calling :py:func:`esper.add_processor`.
    For example::

        my_processor_instance = MyProcessor()
        esper.add_processor(my_processor_instance)

     All the Processors that have been added to the World context will have their
    :py:meth:`esper.Processor.process` methods called by a single call to
    :py:func:`esper.process`. Inside the `process` method is generally where you
    should iterate over Entities with one (or more) calls to the appropriate methods::

        def process(self):
            for ent, (rend, vel) in esper.get_components(Renderable, Velocity):
                your_code_here()
    """

    priority = 0
    sys_processors: _List[esper.Processor] = []

    def add_processor(self, processor_instance: esper.Processor, priority: int = 0) -> None:
        """Add a Processor instance to the current World.

        Add a Processor instance to the world (subclass of
        :py:class:`esper.Processor`), with optional priority.

        When the :py:func:`esper.World.process` function is called,
        Processors with higher priority will be called first.
        """
        processor_instance.priority = priority
        self.sys_processors.append(processor_instance)
        self.sys_processors.sort(key=lambda proc: proc.priority, reverse=True)

    def remove_processor(self, processor_type: _Type[esper.Processor]) -> None:
        """Remove a Processor from the World, by type.

        Make sure to provide the class itself, **not** an instance. For example::

            # OK:
            self.world.remove_processor(MyProcessor)

            # NG:
            self.world.remove_processor(my_processor_instance)

        """
        for processor in self.sys_processors:
            if type(processor) is processor_type:
                self.sys_processors.remove(processor)

    def get_processor(self, processor_type: _Type[esper.Processor]) -> _Optional[esper.Processor]:
        """Get a Processor instance, by type.

        This function returns a Processor instance by type. This could be
        useful in certain situations, such as wanting to call a method on a
        Processor, from within another Processor.
        """
        for processor in self.sys_processors:
            if type(processor) is processor_type:
                return processor
        else:
            return None

    def process(self, *args: _Any, **kwargs: _Any) -> None:
        """Call the process method on all Processors, in order of their priority.

        Call the :py:meth:`esper.Processor.process` method on all assigned
        Processors, respective of their priority. In addition, any Entities
        that were marked for deletion since the last call will be deleted
        at the start of this call.
        """
        esper.clear_dead_entities()
        for processor in self.sys_processors:
            processor.process(*args, **kwargs)

    def systemize(self, *args: _Any, **kwargs: _Any) -> None:
        raise NotImplementedError

###################
#   ECS functions
###################

systems: _List[System] = []

def systemize(*args: _Any, **kwargs: _Any) -> None:
    """Call the process method on all Processors, in order of their priority.

    Call the :py:meth:`esper.Processor.process` method on all assigned
    Processors, respective of their priority. In addition, any Entities
    that were marked for deletion since the last call will be deleted
    at the start of this call.
    """
    esper.process()
    for system in systems:
        system.systemize(*args, **kwargs)
        system.process()

def add_system(system_instance: System, priority: int = 0) -> None:
    """Add a Processor instance to the current World.

    Add a Processor instance to the world (subclass of
    :py:class:`esper.Processor`), with optional priority.

    When the :py:func:`esper.World.process` function is called,
    Processors with higher priority will be called first.
    """
    system_instance.priority = priority
    systems.append(system_instance)
    systems.sort(key=lambda sys: sys.priority, reverse=True)

def remove_system(system_type: _Type[System]) -> None:
    """Remove a Processor from the World, by type.

    Make sure to provide the class itself, **not** an instance. For example::

        # OK:
        self.world.remove_processor(MyProcessor)

        # NG:
        self.world.remove_processor(my_processor_instance)

    """
    for system in systems:
        if type(system) is system_type:
            systems.remove(system)

def get_system(system_type: _Type[System]) -> _Optional[System]:
    """Get a Processor instance, by type.

    This function returns a Processor instance by type. This could be
    useful in certain situations, such as wanting to call a method on a
    Processor, from within another Processor.
    """
    for system in systems:
        if type(system) is system_type:
            return system
    else:
        return None
