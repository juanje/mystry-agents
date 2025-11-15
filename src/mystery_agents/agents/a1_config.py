"""A1: Configuration/Wizard Agent - Collects user preferences."""

from typing import Literal, cast

import click

from mystery_agents.models.state import (
    DifficultyLevel,
    Epoch,
    GameConfig,
    GameState,
    PlayerConfig,
    Theme,
    Tone,
)


class ConfigWizardAgent:
    """
    A1: Config/Wizard Agent.

    Collects user preferences via CLI and populates GameConfig.
    """

    def run(self, state: GameState) -> GameState:
        """
        Run the configuration wizard.

        Args:
            state: Current game state

        Returns:
            Updated game state with populated config
        """
        click.echo("\n=== Mystery Party Game Generator ===\n")
        click.echo("Let's configure your mystery party game!\n")

        # Language
        language = click.prompt(
            "Language / Idioma",
            type=click.Choice(["es", "en"], case_sensitive=False),
            default="es",
        )

        # Country (for name generation)
        country_default = "Spain" if language == "es" else "United States"
        country = click.prompt(
            "Country / País (for character names)",
            default=country_default,
            type=str,
        )

        # Region (optional for more specific cultural context)
        region = click.prompt(
            "\nRegion within country (optional, press Enter to skip)",
            type=str,
            default="",
            show_default=False,
        )
        region = region.strip() or None

        # Epoch
        epochs: list[tuple[int, str, Epoch]] = [
            (1, "modern - Contemporary setting", "modern"),
            (2, "1920s - Roaring Twenties", "1920s"),
            (3, "victorian - Victorian era", "victorian"),
            (4, "custom - Your own setting", "custom"),
        ]
        click.echo("\nAvailable epochs:")
        for num, desc, _ in epochs:
            click.echo(f"  {num}. {desc}")
        epoch_choice = click.prompt("Choose epoch", type=int, default=1)
        epoch = cast(Epoch, next((e for n, _, e in epochs if n == epoch_choice), "modern"))

        custom_epoch_description = None
        if epoch == "custom":
            custom_epoch_description = click.prompt("Describe your custom epoch")

        # Theme
        themes: list[tuple[int, str, Theme]] = [
            (1, "family_mansion - Family gathering in a mansion", "family_mansion"),
            (2, "corporate_retreat - Corporate event", "corporate_retreat"),
            (3, "cruise - Luxury cruise ship", "cruise"),
            (4, "train - Orient Express style train", "train"),
            (5, "custom - Your own theme", "custom"),
        ]
        click.echo("\nAvailable themes:")
        for num, desc, _ in themes:
            click.echo(f"  {num}. {desc}")
        theme_choice = click.prompt("Choose theme", type=int, default=1)
        theme = cast(Theme, next((t for n, _, t in themes if n == theme_choice), "family_mansion"))

        custom_theme_description = None
        if theme == "custom":
            custom_theme_description = click.prompt("Describe your custom theme")

        # Tone is fixed: elegant mystery with wit (Cluedo meets Knives Out)
        tone: Tone = "mystery_party"

        # Player gender distribution
        click.echo("\nNumber of suspect characters (not including host):")
        click.echo("Specify gender distribution (press Enter for balanced 3/3):")
        male = click.prompt("Male characters", type=click.IntRange(0, 10), default=3)
        female = click.prompt("Female characters", type=click.IntRange(0, 10), default=3)

        # Calculate total and validate
        total_players = male + female
        if total_players < 4:
            click.echo(
                "⚠️  Warning: Minimum 4 players required. Adjusting to 4 players (2 male, 2 female)."
            )
            male = 2
            female = 2
            total_players = 4
        elif total_players > 10:
            click.echo(
                "⚠️  Warning: Maximum 10 players allowed. Adjusting to 10 players (5 male, 5 female)."
            )
            male = 5
            female = 5
            total_players = 10

        # Host gender
        click.echo("\nHost gender (the victim character):")
        host_gender_choice = click.prompt(
            "Host gender",
            type=click.Choice(["male", "female"], case_sensitive=False),
            default="male",
        )
        host_gender: Literal["male", "female"] = cast(Literal["male", "female"], host_gender_choice)

        # Duration
        duration = click.prompt(
            "\nGame duration (minutes)",
            type=click.IntRange(60, 180),
            default=90,
        )

        # Difficulty
        difficulties: list[tuple[int, str, DifficultyLevel]] = [
            (1, "easy - Simple mystery, obvious clues", "easy"),
            (2, "medium - Balanced challenge", "medium"),
            (3, "hard - Complex mystery, subtle clues", "hard"),
        ]
        click.echo("\nDifficulty levels:")
        for num, desc, _ in difficulties:
            click.echo(f"  {num}. {desc}")
        difficulty_choice = click.prompt("Choose difficulty", type=int, default=2)
        difficulty = cast(
            DifficultyLevel,
            next((d for n, _, d in difficulties if n == difficulty_choice), "medium"),
        )

        # Create config (dry_run and debug_model come from CLI flags)
        config = GameConfig(
            language=language,
            country=country,
            region=region,
            epoch=epoch,
            custom_epoch_description=custom_epoch_description,
            theme=theme,
            custom_theme_description=custom_theme_description,
            tone=tone,
            players=PlayerConfig(total=total_players, male=male, female=female),
            host_gender=host_gender,
            duration_minutes=duration,
            difficulty=difficulty,
            pre_game_delivery=True,
            dry_run=state.config.dry_run,
            debug_model=state.config.debug_model,
        )

        # Update state
        state.config = config

        click.echo("\n✓ Configuration complete!\n")
        click.echo(f"  Language: {config.language}")
        click.echo(f"  Country: {config.country}")
        if config.region:
            click.echo(f"  Region: {config.region}")
        click.echo(f"  Setting: {config.epoch} / {config.theme}")
        click.echo(f"  Host gender: {config.host_gender}")
        click.echo(
            f"  Players: {config.players.total} ({config.players.male} male, {config.players.female} female)"
        )
        click.echo(f"  Duration: {config.duration_minutes} minutes")
        click.echo(f"  Difficulty: {config.difficulty}")
        click.echo()

        return state
