"""VPS Master Bot - Kirish nuqtasi."""
from __future__ import annotations

import asyncio
import sys
from datetime import time

from loguru import logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, MessageHandler, filters

from bot.config import settings
from bot.database import Database
from bot.middlewares import global_auth_gate, global_auth_gate_callback
from bot.services.scheduler_service import alert_check_job, daily_report_job
from bot.handlers import (
    register_agent_handlers,
    register_ai_handlers,
    register_alert_handlers,
    register_auth_handlers,
    register_backup_handlers,
    register_confirm_handlers,
    register_db_handlers,
    register_docker_handlers,
    register_file_handlers,
    register_git_handlers,
    register_logs_handlers,
    register_media_handlers,
    register_monitoring_handlers,
    register_nginx_handlers,
    register_start_handlers,
    register_system_handlers,
    register_vpn_handlers,
)


async def init_database() -> None:
    """SQLite ma'lumotlar bazasini ishga tushirish."""
    db = Database()
    await db.init()
    logger.info("Ma'lumotlar bazasi ishga tushirildi")


def setup_logging() -> None:
    """Loguru sozlamalari."""
    settings.bot_log_dir.mkdir(parents=True, exist_ok=True)
    log_file = settings.bot_log_dir / "bot.log"

    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    logger.add(
        str(log_file),
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        encoding="utf-8",
    )


def _check_password_configured() -> None:
    if not settings.is_password_configured:
        logger.warning(
            "BOT_PASSWORD_HASH .env faylida sozlanmagan! Bot ishga tushadi, lekin "
            "hech kim kira olmaydi - scripts/gen_password_hash.py orqali hash yarating."
        )


def main() -> None:
    """Asosiy kirish nuqtasi."""
    setup_logging()
    logger.info("VPS Master Bot ishga tushirilmoqda...")
    _check_password_configured()

    # Ma'lumotlar bazasini ishga tushirish
    asyncio.run(init_database())

    # Ilovani yaratish
    application = (
        ApplicationBuilder()
        .token(settings.telegram_bot_token)
        .build()
    )

    # --- group=-1: global auth gate (parol/sessiya tekshiruvi) ---
    # Bu HAR BIR update uchun barcha boshqa handlerlardan OLDIN ishlaydi.
    # Sessiya yo'q bo'lsa ApplicationHandlerStop ko'tariladi va update
    # pastdagi (group=0) hech qanday handlerga yetib bormaydi.
    application.add_handler(MessageHandler(filters.ALL, global_auth_gate), group=-1)
    application.add_handler(CallbackQueryHandler(global_auth_gate_callback, pattern=".*"), group=-1)

    # --- group=0: haqiqiy funksional handlerlar ---
    register_start_handlers(application)
    register_auth_handlers(application)
    register_confirm_handlers(application)
    register_alert_handlers(application)
    register_ai_handlers(application)
    register_docker_handlers(application)
    register_monitoring_handlers(application)
    register_file_handlers(application)
    register_vpn_handlers(application)
    register_media_handlers(application)
    register_git_handlers(application)
    register_backup_handlers(application)
    register_system_handlers(application)
    register_nginx_handlers(application)
    register_db_handlers(application)
    register_logs_handlers(application)
    if settings.enable_agent:
        register_agent_handlers(application)  # eng oxirida: erkin matn uchun "catch-all"
    else:
        logger.info("ENABLE_AGENT=false - erkin matn routeri o'chirilgan.")

    # --- Fon vazifalari: kunlik hisobot va threshold alertlar ---
    if application.job_queue is None:
        logger.warning(
            "JobQueue mavjud emas (python-telegram-bot[job-queue] o'rnatilmagan?) - "
            "kunlik hisobot va alertlar ishlamaydi."
        )
    else:
        if settings.enable_daily_report:
            try:
                from zoneinfo import ZoneInfo
                tz = ZoneInfo(settings.bot_timezone)
            except Exception:
                tz = None
            report_time = time(hour=settings.daily_report_hour, minute=0, tzinfo=tz)
            application.job_queue.run_daily(daily_report_job, time=report_time, name="daily_report")
            logger.info(f"Kunlik hisobot {settings.daily_report_hour}:00 ga rejalashtirildi")

        if settings.enable_alerts:
            application.job_queue.run_repeating(
                alert_check_job,
                interval=settings.alert_check_interval_seconds,
                first=10,
                name="alert_check",
            )
            logger.info(
                f"Alert tekshiruvi har {settings.alert_check_interval_seconds}s da ishga tushadi"
            )

    # Botni ishga tushirish
    if settings.telegram_webhook_url:
        logger.info(f"Webhook {settings.webhook_port} portda ishga tushirilmoqda")
        application.run_webhook(
            listen="0.0.0.0",
            port=settings.webhook_port,
            webhook_url=settings.telegram_webhook_url,
        )
    else:
        logger.info("Polling rejimi ishga tushirilmoqda...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
