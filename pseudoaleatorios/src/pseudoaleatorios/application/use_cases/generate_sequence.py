from __future__ import annotations

import logging

from ...domain.models.generator_config import GeneratorConfig, GeneratorResult
from ...domain.ports.generator import PseudorandomGeneratorPort
from ...infrastructure.analysis.statistics import StatisticalReport, full_report

logger = logging.getLogger(__name__)


class GenerateSequenceUseCase:
    def __init__(self, generator: PseudorandomGeneratorPort) -> None:
        self._generator = generator

    def execute(
        self,
        config: GeneratorConfig,
        run_statistics: bool = True,
    ) -> tuple[GeneratorResult, StatisticalReport | None]:
        logger.info(
            "Generating %d values with %s (seed=%d)",
            config.count,
            self._generator.method_name,
            config.seed,
        )
        result = self._generator.generate(config)

        if result.period is not None:
            logger.warning(
                "Period detected at n=%d — sequence will repeat after this point.",
                result.period,
            )
        else:
            logger.info("No period detected within the generated sequence.")

        report: StatisticalReport | None = None
        if run_statistics:
            report = full_report(result.normalized)
            logger.info(
                "Statistics — mean=%.4f  std=%.4f  chi2=%.3f (%s)  runs z=%.3f (%s)",
                report.mean,
                report.std,
                report.uniformity.statistic,
                "PASS" if report.uniformity.passed else "FAIL",
                report.runs.z_statistic,
                "PASS" if report.runs.passed else "FAIL",
            )

        return result, report
