from pathlib import Path
import subprocess


class SirilRunner:

    def __init__(self, siril_path: str):

        # ==========================
        # Siril executable
        # ==========================

        self.siril = Path(
            siril_path
        ).resolve()


        if not self.siril.exists():

            raise FileNotFoundError(
                f"Siril introuvable : {self.siril}"
            )


        if self.siril.is_dir():

            raise ValueError(
                "Le chemin Siril pointe vers un dossier"
            )


        # ==========================
        # Scripts Siril
        # ==========================

        self.script_dir = (
            Path(__file__).parent.parent
            / "scripts"
        )


        if not self.script_dir.exists():

            raise FileNotFoundError(
                f"Dossier scripts introuvable : {self.script_dir}"
            )


        # ==========================
        # Sécurité CLI
        # ==========================

        if "siril-cli" not in self.siril.name.lower():

            print(
                "⚠️ Attention : utilise siril-cli.exe pour un pipeline fiable"
            )



    # =====================================================
    # Lancement générique d'un script Siril
    # =====================================================

    def run(
        self,
        script: Path,
        workdir: Path,
        callback=None
    ):


        script = Path(
            script
        ).resolve()


        workdir = Path(
            workdir
        ).resolve()



        if not script.exists():

            raise FileNotFoundError(
                f"Script introuvable : {script}"
            )


        if not workdir.exists():

            raise FileNotFoundError(
                f"Workdir introuvable : {workdir}"
            )



        command = [

            str(self.siril),

            "-d",
            str(workdir),

            "-s",
            str(script)

        ]



        print("\n🚀 RUN SIRIL")

        print(
            "EXE    :",
            self.siril
        )

        print(
            "SCRIPT :",
            script
        )

        print(
            "DIR    :",
            workdir
        )



        process = subprocess.Popen(

            command,

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,

            text=True,

            encoding="utf-8",

            errors="replace",

            shell=False

        )



        logs = []

        error_detected = False



        for line in process.stdout:


            line = line.rstrip()


            logs.append(
                line
            )


            if (
                "ERROR" in line.upper()
                or
                "ERREUR" in line.upper()
            ):

                error_detected = True



            if callback:

                callback(
                    line
                )



        process.wait()



        success = (

            process.returncode == 0

            and not error_detected

        )



        return success, logs




    # =====================================================
    # Analyse qualité
    # =====================================================

    def analyse(
        self,
        workdir: Path,
        callback=None
    ):


        script = (
            self.script_dir
            /
            "Analyse_Qualite.ssf"
        )


        return self.run(

            script,

            workdir,

            callback

        )



    # =====================================================
    # Alignement des lights
    # =====================================================

    def alignement(
        self,
        workdir: Path,
        callback=None
    ):


        script = (
            self.script_dir
            /
            "Alignement_lights.ssf"
        )


        return self.run(

            script,

            workdir,

            callback

        )



    # =====================================================
    # Traitement final
    # =====================================================

    def traitement(
        self,
        mode: str,
        workdir: Path,
        callback=None
    ):


        scripts = {


            "LRGB":
                "Traitement_LRGB.ssf",


            "SHO":
                "Traitement_SHO.ssf",


            "LSHO":
                "Traitement_LSHO.ssf"

        }



        if mode not in scripts:

            raise ValueError(

                f"Mode inconnu : {mode}"

            )



        script = (

            self.script_dir

            /

            scripts[mode]

        )



        return self.run(

            script,

            workdir,

            callback

        )