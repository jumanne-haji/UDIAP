"""
Seed script – creates sample assessment + admin user.
Run: python -m seed  (from backend/ with PYTHONPATH set)
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.assessment import Assessment, Question, AssessmentCategory, DifficultyLevel
from app.core.security import get_password_hash


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Admin user
        admin = User(
            name="UDIAP Admin",
            email="admin@udiap.ai",
            password_hash=get_password_hash("Admin@12345"),
            role=UserRole.SUPERADMIN,
        )
        db.add(admin)

        # Demo user
        demo = User(
            name="Demo Researcher",
            email="demo@udiap.ai",
            password_hash=get_password_hash("Demo@12345"),
            role=UserRole.USER,
        )
        db.add(demo)

        # Sample Assessment
        assessment = Assessment(
            title="Strategic Technology Decision Scenario",
            description=(
                "You are the CTO of a mid-size fintech company. "
                "A critical infrastructure decision must be made under uncertainty."
            ),
            category=AssessmentCategory.STRATEGIC,
            difficulty=DifficultyLevel.ADVANCED,
            estimated_minutes=25,
        )
        db.add(assessment)
        await db.flush()

        q1 = Question(
            assessment_id=assessment.id,
            question_text=(
                "Your payment processing system is approaching capacity. "
                "You must choose between: (A) scaling the current monolithic architecture, "
                "(B) migrating to a microservices + event-driven design, or "
                "(C) adopting a managed cloud payment service. "
                "The board needs a decision in 48 hours. Budget is constrained. "
                "Regulatory compliance (PCI-DSS) is non-negotiable.\n\n"
                "Provide a structured recommendation that demonstrates your decision process."
            ),
            context="Fintech, high-transaction environment, 18-month growth forecast of 3x.",
            constraints="Budget < $400k, 6-month implementation window preferred, zero downtime required.",
            expected_skills="critical_thinking,risk_management,technical_reasoning,communication",
            order_index=1,
        )
        db.add(q1)

        assessment2 = Assessment(
            title="Ethical AI Deployment Dilemma",
            description="Evaluate the deployment of an AI credit-scoring model with potential bias.",
            category=AssessmentCategory.ETHICAL,
            difficulty=DifficultyLevel.INTERMEDIATE,
            estimated_minutes=20,
        )
        db.add(assessment2)
        await db.flush()

        q2 = Question(
            assessment_id=assessment2.id,
            question_text=(
                "Your team has trained a high-accuracy credit scoring model. "
                "Internal audit shows it performs 12% worse for applicants from certain "
                "demographic groups. Business pressure is high to ship. "
                "How do you proceed? Detail your reasoning and decision process."
            ),
            context="Regulated financial institution, existing model is 4 years old and underperforming.",
            constraints="Model must be explainable, fairness metrics required by regulator.",
            expected_skills="critical_thinking,risk_management,reflection,communication",
            order_index=1,
        )
        db.add(q2)

        await db.commit()
        print("✅ Seed completed successfully")
        print("   Admin: admin@udiap.ai / Admin@12345")
        print("   Demo:  demo@udiap.ai  / Demo@12345")


if __name__ == "__main__":
    asyncio.run(seed())
