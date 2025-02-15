:class:`CompartmentedModel`: Compartmented models of disease
============================================================

.. currentmodule:: epydemic

.. autoclass:: CompartmentedModel
   :show-inheritance:

Compartmented models are designed so that their specification is
independent of the :term:`process dynamics` used to simulate them:
they can be run in :term:`discrete time` using :term:`synchronous dynamics`,
or in :term:`continuous time` using :term:`stochastic dynamics`.

:class:`CompartmentedModel` is an abstract class that must be
sub-classed to define actual disease models. `epydemic` provides
implementations of the two "reference" compartmented models,
:class:`SIR` and :class:`SIS`, as well as several variants of them:
:ref:`Hethcote <Het00>` provides a survey of a huge range of others.


Attributes
----------

.. autoattribute:: CompartmentedModel.COMPARTMENT

.. autoattribute:: CompartmentedModel.OCCUPIED


Model setup
-----------

Immediately before being run, the model is set up by placing all the
nodes into compartments. All edges are also marked as unoccupied.

.. automethod:: CompartmentedModel.reset

.. automethod:: CompartmentedModel.build

.. automethod:: CompartmentedModel.setUp

.. automethod:: CompartmentedModel.initialCompartmentDistribution

.. automethod:: CompartmentedModel.initialCompartments

.. automethod:: CompartmentedModel.changeInitialCompartment


Building and querying the model
-------------------------------

Building a model (within :meth:`CompartmentedModel.build`) means specifying
the various compartments, loci, and events, and their associated probabilities.
The initial occupancy of compartments can be set to allow for random initialisation,
and the occupancy of existing components changed to allow better sub-classing.

.. automethod:: CompartmentedModel.addCompartment

. automethod:: CompartmentedModel.changeCompartmentInitialOccupancy

.. automethod:: CompartmentedModel.trackNodesInCompartment

.. automethod:: CompartmentedModel.trackEdgesBetweenCompartments

We can also query the model, which is especially useful within event functions
and when generating results in :meth:`CompartmentedModel.results`

.. automethod:: CompartmentedModel.compartments

.. automethod:: CompartmentedModel.compartment


Evolving the network
--------------------

Events in compartmented models need an interafce to change the compartment of nodes
and to mark edges used in transmitting the epidemic.

.. automethod:: CompartmentedModel.setCompartment

.. automethod:: CompartmentedModel.getCompartment

.. automethod:: CompartmentedModel.changeCompartment

.. automethod:: CompartmentedModel.markOccupied

The network access interface of :class:`Process` is extended with methods that
understand the mappings between nodes, edges, and compartments.

.. automethod:: CompartmentedModel.addNode

.. automethod:: CompartmentedModel.removeNode

.. automethod:: CompartmentedModel.addEdge

.. automethod:: CompartmentedModel.removeEdge


Generating results
------------------

The experiment needs to define a results dict to return when it completes.

.. automethod:: CompartmentedModel.results

.. automethod:: CompartmentedModel.skeletonise
