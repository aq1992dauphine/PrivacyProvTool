## notes of my supervisor

At the moment, the walkthrough mainly demonstrates manually that the annotations propagate correctly through the pipeline. I think we can now build on this and turn it into a more systematic evaluation.

For example, the walkthrough already implicitly shows that privacy annotations propagate correctly across transformation, that provenance relationships are maintained, that governance obligations can be traced through the workflow. These are actually good evaluation dimensions.

One thing that I think will be important for reviewers is the question of generalisability. Right now the example feels a bit tied to one handcrafted use case, so I think we should either show that the implementation can work on more general Python data pipelines or clearly define the class of supported workflows/scripts. For example, pandas pipelines, scikit-learn workflows, or another specific class.  Otherwise reviewers may ask whether the framework only works for this specific example.

I also think the evaluation could include a few different pipeline examples instead of only one. Even 3–5 relatively small workflows would already help demonstrate that the approach is not tied to a single use case.

Another thing that could strengthen the evaluation is to separate clearly what is manually annotated, what is automatically generated, and what is inferred through propagation rules.



What I'm suggesting is to create an implementation that works for a class of Python scripts (dataframes, scikit‑learn, etc.). For the evaluation, it would be good to apply this implementation to 3 to 5 use cases to demonstrate both the benefits and the limitations of the approach. The use case from the walkthrough could be one of them.

I'm not sure that a single use case will be sufficient for the Wise conference. I published there a very long time ago. If the audience is mostly computer scientists (as opposed to applied scientists), they would likely prefer something generalizable rather than something tightly tied to a single use case.

My suggestion: start with the implementation to see whether what you've done manually can be reproduced using a tool you develop. Then try that same tool on 3 or more use cases, even if they are simple.





### Expected package structure


privacyprov/
  core/
    enums.py
    models.py
    graph.py

  instrumentation/
    context.py

  privacy/
    annotation.py
    annotation_loader.py
    operation_policy_loader.py
    ontology.py
    propagation_engine.py
    operator_rules.py

  queries/
    erasure_impact.py
    sensitivity_exposure.py
    transformation_responsibility.py
    consent_compliance.py
    role_filter.py

  examples/
    asd_workflow_instrumented.py
    census_workflow.py
    compas_workflow.py
    german_credit_workflow.py

  outputs/



### Coding style
    Keep code simple and explicit.
    Prefer dataclasses.
    Avoid over-engineering.
    Every StepRun should have stable IDs.
    Every artifact should have stable IDs.
    Export JSON and CSV.
    CSV should be compatible with Neo4j-style import or MLProvLens-style graph loading.
    Add docstrings to public classes and functions.


    