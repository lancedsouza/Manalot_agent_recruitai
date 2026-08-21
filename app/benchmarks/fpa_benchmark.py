from app.models.role_benchmark import (
    BenchmarkDimension,
    RoleBenchmark,EvalutionCriteriria
)


FPA_BENCHMARK = RoleBenchmark(
    function="FP&A",

    dimensions=[
        BenchmarkDimension(
            name="Scope and Scale",
            description=(
                "Evaluate portfolio, P&L, revenue, budget, "
                "business-unit and geographic scope actually owned."
            ),
            weight=0.20,
        ),

        BenchmarkDimension(
            name="FP&A Core Depth",
            description=(
                "Evaluate forecasting, AOP, variance analysis, "
                "financial modeling, planning ownership and "
                "full P&L analytical depth."
            ),
            weight=0.20,
        ),

        BenchmarkDimension(
            name="Stakeholder Altitude",
            description=(
                "Evaluate the seniority of stakeholders the "
                "candidate regularly presents to, partners with "
                "or influences."
            ),
            weight=0.15,
        ),

        BenchmarkDimension(
            name="Systems and Transformation",
            description=(
                "Evaluate finance-system expertise and ownership "
                "of automation or transformation initiatives, "
                "including tools such as Power BI, SAP, Hyperion, "
                "Anaplan, Python, RPA and Data Lake."
            ),
            weight=0.15,
        ),

        BenchmarkDimension(
            name="Leadership",
            description=(
                "Evaluate direct and indirect team leadership, "
                "people-management scope and organizational "
                "responsibility."
            ),
            weight=0.10,
        ),

        BenchmarkDimension(
            name="Career Trajectory",
            description=(
                "Evaluate progression in responsibility, scope, "
                "seniority and career consistency over time."
            ),
            weight=0.10,
        ),

        BenchmarkDimension(
            name="Qualification and Domain Strength",
            description=(
                "Evaluate relevant finance qualifications, "
                "education, domain expertise and professional depth."
            ),
            weight=0.10,
        ),
    ],
)