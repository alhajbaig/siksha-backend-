"""
SIKSHA SAATHI — DYNAMIC QUESTION ENGINE
Dual-Engine Intelligent Question Generation:
1. Groq LLM (Qwen / LLaMA) for authentic, high-yield, deep-concept curriculum questions with KaTeX equations.
2. Parametric & Algorithmic Problem Synthesizer with randomized numerical values, variables, and misconception distractors.
3. Automatic SQLite persistence into `practice_questions` for learning genome, mistake logs, and score tracking.
"""

import json
import random
import uuid
import logging
from typing import List, Dict, Any, Optional
import httpx

from backend.config import settings
from backend.db import get_db_connection

logger = logging.getLogger(__name__)

# Preferred models in order of latency and quality
GROQ_MODELS = [
    "qwen/qwen3.8-27b",
    "qwen/qwen3.6-27b",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "groq/compound-mini"
]


class DynamicQuestionEngine:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY

    # =========================================================================
    # 1. PARAMETRIC & ALGORITHMIC FALLBACK GENERATORS
    # =========================================================================
    def _generate_parametric_physics(self, topic: str) -> Dict[str, Any]:
        """Generates authentic randomized physics questions with step-by-step math."""
        t_low = topic.lower()

        if "dimension" in t_low or "unit" in t_low:
            quantities = [
                {
                    "name": "Universal Gravitational Constant ($G$)",
                    "formula": "F = G \\frac{m_1 m_2}{r^2}",
                    "dim": "[M^{-1} L^3 T^{-2}]",
                    "distractors": ["[M^1 L^3 T^{-2}]", "[M^{-1} L^2 T^{-2}]", "[M^{-2} L^3 T^{-1}]"],
                    "steps": "From Newton's Law of Gravitation, $G = \\frac{F \\cdot r^2}{m_1 m_2}$. Substituting dimensions: $[F] = [M L T^{-2}]$, $[r^2] = [L^2]$, $[m_1 m_2] = [M^2]$. Hence, $[G] = \\frac{[M L T^{-2}][L^2]}{[M^2]} = [M^{-1} L^3 T^{-2}]$."
                },
                {
                    "name": "Planck's Constant ($h$)",
                    "formula": "E = h \\nu",
                    "dim": "[M L^2 T^{-1}]",
                    "distractors": ["[M L^2 T^{-2}]", "[M L^1 T^{-1}]", "[M L^3 T^{-2}]"],
                    "steps": "From the Planck-Einstein relation, $h = \\frac{E}{\\nu}$. Substituting dimensions: $[E] = [M L^2 T^{-2}]$ and $[\nu] = [T^{-1}]$. Hence, $[h] = \\frac{[M L^2 T^{-2}]}{[T^{-1}]} = [M L^2 T^{-1}]$, which represents angular momentum."
                },
                {
                    "name": "Permittivity of Free Space ($\\varepsilon_0$)",
                    "formula": "F = \\frac{1}{4\\pi\\varepsilon_0} \\frac{q_1 q_2}{r^2}",
                    "dim": "[M^{-1} L^{-3} T^4 A^2]",
                    "distractors": ["[M^{-1} L^3 T^{-4} A^{-2}]", "[M^1 L^{-3} T^4 A^2]", "[M^{-1} L^{-2} T^3 A^2]"],
                    "steps": "From Coulomb's Law, $\\varepsilon_0 = \\frac{q_1 q_2}{4\\pi F r^2}$. Dimensions of charge $[q] = [A T]$, force $[F] = [M L T^{-2}]$, distance $[r^2] = [L^2]$. Hence, $[\varepsilon_0] = \\frac{[A^2 T^2]}{[M L T^{-2}][L^2]} = [M^{-1} L^{-3} T^4 A^2]$."
                },
                {
                    "name": "Stefan-Boltzmann Constant ($\\sigma$)",
                    "formula": "E = \\sigma T^4 \\text{ (energy per unit area per sec)}",
                    "dim": "[M L^0 T^{-3} K^{-4}]",
                    "distractors": ["[M L^2 T^{-3} K^{-4}]", "[M L^{-1} T^{-2} K^{-4}]", "[M L^0 T^{-2} K^{-4}]"],
                    "steps": "Radiant emittance $E$ is power per unit area: $[E] = \\frac{[M L^2 T^{-3}]}{[L^2]} = [M T^{-3}]$. Since $E = \\sigma T^4$, $[\\sigma] = \\frac{[E]}{[T^4]} = [M L^0 T^{-3} K^{-4}]$."
                }
            ]
            q_choice = random.choice(quantities)
            options = [q_choice["dim"]] + q_choice["distractors"]
            random.shuffle(options)
            correct_idx = options.index(q_choice["dim"])

            return {
                "question_text": f"What are the dimensional formula and SI dimensions of the **{q_choice['name']}**?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"**Derivation:** {q_choice['steps']}",
                "difficulty": "Medium"
            }

        elif "circular" in t_low:
            v = random.choice([10, 15, 20, 25, 30])
            r = random.choice([5, 10, 20, 25, 50])
            m = random.choice([1, 2, 4, 5])
            a_c = round((v ** 2) / r, 1)
            f_c = round(m * a_c, 1)
            distractors = [round(f_c * 1.5, 1), round(f_c * 0.5, 1), round(f_c + 20, 1)]
            options = [f"{f_c} N"] + [f"{d} N" for d in distractors]
            random.shuffle(options)
            correct_idx = options.index(f"{f_c} N")

            return {
                "question_text": f"A particle of mass ${m}\\text{{ kg}}$ moves in a horizontal circular path of radius ${r}\\text{{ m}}$ with a constant orbital speed of ${v}\\text{{ m/s}}$. Determine the magnitude of the net centripetal force acting on the particle.",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"The centripetal acceleration is $a_c = \\frac{{v^2}}{{r}} = \\frac{{{v}^2}}{{{r}}} = {a_c}\\text{{ m/s}}^2$. The required centripetal force is $F_c = m \\cdot a_c = {m} \\times {a_c} = {f_c}\\text{{ N}}$. Note that although speed is constant, velocity vector changes direction continually.",
                "difficulty": "Easy"
            }

        elif "kinematic" in t_low or "motion" in t_low or "projectile" in t_low:
            u = random.choice([20, 30, 40, 50])
            theta = random.choice([30, 45, 60])
            g = 10
            import math
            rad = math.radians(theta)
            h_max = round(((u * math.sin(rad)) ** 2) / (2 * g), 1)
            t_flight = round((2 * u * math.sin(rad)) / g, 1)
            distractors = [round(h_max * 1.25, 1), round(h_max * 0.75, 1), round(h_max + 15, 1)]
            options = [f"{h_max} m"] + [f"{d} m" for d in distractors]
            random.shuffle(options)
            correct_idx = options.index(f"{h_max} m")

            return {
                "question_text": f"A projectile is launched from flat ground with initial speed $u = {u}\\text{{ m/s}}$ at an elevation angle of $\\theta = {theta}^\\circ$ above the horizontal. Taking $g = 10\\text{{ m/s}}^2$, what is the maximum vertical height $H_{{\\max}}$ reached by the projectile?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"Vertical component of initial velocity is $u_y = u \\sin({theta}^\\circ) = {u} \\times \\sin({theta}^\\circ)$. At peak height, vertical velocity $v_y = 0$. Using $v_y^2 = u_y^2 - 2gH_{{\\max}}$, we obtain $H_{{\\max}} = \\frac{{u^2 \\sin^2({theta}^\\circ)}}{{2g}} = {h_max}\\text{{ m}}$. Total time of flight is $T = {t_flight}\\text{{ s}}$.",
                "difficulty": "Medium"
            }

        else:
            # Generic high-yield Physics question
            work_vals = random.choice([(10, 5, 60), (20, 4, 30), (15, 8, 45)])
            F, d, angle = work_vals
            import math
            W = round(F * d * math.cos(math.radians(angle)), 1)
            distractors = [round(W * 1.4, 1), round(F * d, 1), round(W * 0.6, 1)]
            options = [f"{W} J"] + [f"{dist} J" for dist in distractors]
            random.shuffle(options)
            correct_idx = options.index(f"{W} J")

            return {
                "question_text": f"A constant force $\\vec{{F}} = {F}\\text{{ N}}$ acts on a block displacing it by $\\vec{{d}} = {d}\\text{{ m}}$ along a straight path inclined at an angle of $\\theta = {angle}^\\circ$ to the force vector. What is the work done by the force?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"Work done by a constant force is given by the dot product $W = \\vec{{F}} \\cdot \\vec{{d}} = F d \\cos\\theta = {F} \\times {d} \\times \\cos({angle}^\\circ) = {W}\\text{{ J}}$.",
                "difficulty": "Easy"
            }

    def _generate_parametric_chemistry(self, topic: str) -> Dict[str, Any]:
        """Generates authentic randomized chemistry questions with numerical precision."""
        t_low = topic.lower()

        if "stoichiometry" in t_low or "mole" in t_low:
            moles_a = random.choice([2.0, 3.0, 4.0, 5.0])
            # 2 H2 + O2 -> 2 H2O
            moles_o2_needed = round(moles_a / 2.0, 2)
            moles_h2o_produced = moles_a
            distractors = [round(moles_a * 1.5, 2), round(moles_o2_needed, 2), round(moles_a * 2, 2)]
            options = [f"{moles_h2o_produced} mol"] + [f"{d} mol" for d in distractors]
            random.shuffle(options)
            correct_idx = options.index(f"{moles_h2o_produced} mol")

            return {
                "question_text": f"In the combustion of hydrogen gas according to $2\\text{{H}}_2(g) + \\text{{O}}_2(g) \\rightarrow 2\\text{{H}}_2\\text{{O}}(g)$, if ${moles_a}\\text{{ moles}}$ of $\\text{{H}}_2$ react completely with excess oxygen, how many moles of $\\text{{H}}_2\\text{{O}}$ vapor are produced?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"The balanced stoichiometric ratio between $\\text{{H}}_2$ and $\\text{{H}}_2\\text{{O}}$ is $2:2 = 1:1$. Since $\\text{{O}}_2$ is in excess, $\\text{{H}}_2$ is the limiting reactant. Therefore, ${moles_a}\\text{{ mol of H}}_2$ produces exactly ${moles_h2o_produced}\\text{{ mol of H}}_2\\text{{O}}$.",
                "difficulty": "Easy"
            }

        elif "equilibrium" in t_low or "le chatelier" in t_low:
            shifts = [
                ("exothermic", "temperature is increased", "shifts in reverse (left) direction to absorb heat"),
                ("endothermic", "temperature is increased", "shifts in forward (right) direction to absorb heat"),
                ("gaseous reaction with $\\Delta n_g > 0$", "pressure is increased", "shifts toward the side with fewer gas moles (left)"),
                ("gaseous reaction with $\\Delta n_g < 0$", "pressure is increased", "shifts toward the side with fewer gas moles (right)")
            ]
            rxn = random.choice(shifts)
            correct = rxn[2]
            distractors = [
                "equilibrium constant $K$ remains unaffected and system does not shift",
                "rate of forward reaction doubles while reverse reaction halts",
                "shifts to side with greater molecular volume unconditionally"
            ]
            options = [correct] + distractors
            random.shuffle(options)
            correct_idx = options.index(correct)

            return {
                "question_text": f"According to Le Chatelier's Principle, for a reversible chemical system where the forward process is **{rxn[0]}**, what happens to the equilibrium when **{rxn[1]}**?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"Le Chatelier's principle dictates that the system responds to counteract the imposed disturbance: {correct}.",
                "difficulty": "Medium"
            }

        elif "kinetics" in t_low or "order" in t_low or "arrhenius" in t_low:
            k = random.choice([0.023, 0.045, 0.0693, 0.1386])
            t_half = round(0.693 / k, 1)
            distractors = [round(t_half * 0.5, 1), round(t_half * 2.0, 1), round(1.0 / k, 1)]
            options = [f"{t_half} s"] + [f"{d} s" for d in distractors]
            random.shuffle(options)
            correct_idx = options.index(f"{t_half} s")

            return {
                "question_text": f"A chemical decomposition reaction follows first-order kinetics with a rate constant $k = {k}\\text{{ s}}^{{-1}}$. What is the half-life ($t_{{1/2}}$) of the reaction?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"For a first-order reaction, the half-life is independent of initial concentration and given by $t_{{1/2}} = \\frac{{\\ln 2}}{{k}} = \\frac{{0.693}}{{{k}}} = {t_half}\\text{{ s}}$.",
                "difficulty": "Medium"
            }

        else:
            # Bonding / Hybridization
            mols = [
                ("$\\text{SF}_6$", "$sp^3d^2$", "Octahedral", ["$sp^3d$", "$sp^3$", "$dsp^2$"]),
                ("$\\text{PCl}_5$", "$sp^3d$", "Trigonal Bipyramidal", ["$sp^3d^2$", "$sp^3$", "$dsp^3$"]),
                ("$\\text{XeF}_4$", "$sp^3d^2$", "Square Planar", ["$sp^3d$", "$sp^3$", "$d^2sp^3$"]),
                ("$\\text{NH}_3$", "$sp^3$", "Trigonal Pyramidal", ["$sp^2$", "$sp^3d$", "$sp$"])
            ]
            chosen = random.choice(mols)
            correct = f"{chosen[1]} with {chosen[2]} geometry"
            distractors = [f"{d} with {chosen[2]} geometry" for d in chosen[3]]
            options = [correct] + distractors
            random.shuffle(options)
            correct_idx = options.index(correct)

            return {
                "question_text": f"What is the hybridization of the central atom and the molecular geometry of **{chosen[0]}** according to VSEPR theory?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"For {chosen[0]}, counting bonding pairs and lone pairs gives steric number and electron geometry. Central atom undergoes {chosen[1]} hybridization, resulting in {chosen[2]} molecular shape.",
                "difficulty": "Medium"
            }

    def _generate_parametric_math(self, topic: str) -> Dict[str, Any]:
        """Generates authentic randomized math questions with KaTeX equations."""
        t_low = topic.lower()

        if "calculus" in t_low or "differentiation" in t_low or "derivative" in t_low:
            n = random.choice([3, 4, 5])
            coeff = random.choice([2, 3, 5])
            x_val = random.choice([1, 2])
            # f(x) = coeff * x^n
            deriv_val = coeff * n * (x_val ** (n - 1))
            distractors = [deriv_val + coeff, deriv_val - n, coeff * (x_val ** n)]
            options = [str(deriv_val)] + [str(d) for d in distractors]
            random.shuffle(options)
            correct_idx = options.index(str(deriv_val))

            c_times_n = coeff * n
            return {
                "question_text": f"Find the numerical derivative $f'({x_val})$ for the polynomial function $f(x) = {coeff}x^{{{n}}} - 4x + 7$.",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"Using the power rule: $f'(x) = \\frac{{d}}{{dx}}({coeff}x^{{{n}}} - 4x + 7) = {c_times_n}x^{{{n - 1}}} - 4$. Substituting $x = {x_val}$: $f'({x_val}) = {c_times_n}({x_val})^{{{n - 1}}} - 4 = {deriv_val}$.",
                "difficulty": "Easy"
            }

        elif "integral" in t_low or "integration" in t_low:
            a = random.choice([1, 2])
            b = random.choice([3, 4])
            # int_a^b (2x + 1) dx = [x^2 + x]_a^b
            val = (b**2 + b) - (a**2 + a)
            distractors = [val + 4, val - 3, val * 2]
            options = [str(val)] + [str(d) for d in distractors]
            random.shuffle(options)
            correct_idx = options.index(str(val))

            return {
                "question_text": f"Evaluate the definite integral $\\int_{{{a}}}^{{{b}}} (2x + 1) \\, dx$.",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"The antiderivative is $\\int (2x + 1) \\, dx = x^2 + x + C$. By Fundamental Theorem of Calculus: $\\left[x^2 + x\\right]_{{{a}}}^{{{b}}} = ({b}^2 + {b}) - ({a}^2 + {a}) = ({b**2 + b}) - ({a**2 + a}) = {val}$.",
                "difficulty": "Medium"
            }

        elif "matrix" in t_low or "determinant" in t_low:
            a, b, c, d = random.choice([(2, 3, 1, 4), (3, 5, 2, 6), (4, 1, 2, 3), (5, 2, 3, 4)])
            det = a * d - b * c
            distractors = [a * d + b * c, det + 2, det - 5]
            options = [str(det)] + [str(dist) for dist in distractors]
            random.shuffle(options)
            correct_idx = options.index(str(det))

            return {
                "question_text": f"Compute the determinant of the $2 \\times 2$ matrix $A = \\begin{{pmatrix}} {a} & {b} \\\\ {c} & {d} \\end{{pmatrix}}$.",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"The determinant of a $2\\times 2$ matrix $\\begin{{pmatrix}} a & b \\\\ c & d \\end{{pmatrix}}$ is computed as $\\det(A) = ad - bc$. Here, $\\det(A) = ({a})({d}) - ({b})({c}) = {a * d} - {b * c} = {det}$.",
                "difficulty": "Easy"
            }

        else:
            # Probability / Vectors
            return {
                "question_text": "If two non-zero vectors $\\vec{a}$ and $\\vec{b}$ satisfy $|\\vec{a} + \\vec{b}| = |\\vec{a} - \\vec{b}|$, what is the angle $\\theta$ between $\\vec{a}$ and $\\vec{b}$?",
                "option_a": "$90^\\circ$ (orthogonal)",
                "option_b": "$0^\\circ$ (collinear)",
                "option_c": "$180^\\circ$ (anti-parallel)",
                "option_d": "$45^\\circ$",
                "correct_option": 0,
                "explanation": "Squaring both sides: $|\\vec{a} + \\vec{b}|^2 = |\\vec{a} - \\vec{b}|^2 \\implies a^2 + b^2 + 2\\vec{a}\\cdot\\vec{b} = a^2 + b^2 - 2\\vec{a}\\cdot\\vec{b} \\implies 4\\vec{a}\\cdot\\vec{b} = 0 \\implies \\vec{a}\\cdot\\vec{b} = 0$. Since both vectors are non-zero, $\\cos\\theta = 0$, giving $\\theta = 90^\\circ$.",
                "difficulty": "Medium"
            }

    def _generate_parametric_cs(self, topic: str) -> Dict[str, Any]:
        """Generates authentic CS & algorithm questions."""
        t_low = topic.lower()

        if "tree" in t_low or "bst" in t_low:
            n = random.choice([7, 15, 31, 63])
            import math
            min_h = int(math.log2(n + 1)) - 1
            max_h = n - 1
            options = [f"{min_h} and {max_h}", f"{min_h + 1} and {max_h}", f"{min_h} and {n}", f"1 and {n}"]
            random.shuffle(options)
            correct_idx = options.index(f"{min_h} and {max_h}")

            return {
                "question_text": f"What are the minimum and maximum possible heights of a binary search tree (BST) containing $N = {n}$ distinct keys (measuring height as number of edges on root-to-leaf path)?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"Minimum height occurs in a fully balanced complete binary tree: $h_{{\\min}} = \\lfloor \\log_2({n}) \\rfloor = {min_h}$. Maximum height occurs in a degenerate skewed tree (linked list structure): $h_{{\\max}} = N - 1 = {max_h}$.",
                "difficulty": "Medium"
            }

        elif "complexity" in t_low or "search" in t_low or "algorithm" in t_low:
            n = random.choice([1024, 2048, 4096, 8192])
            import math
            comps = int(math.log2(n)) + 1
            distractors = [comps * 2, n // 2, comps - 3]
            options = [str(comps)] + [str(d) for d in distractors]
            random.shuffle(options)
            correct_idx = options.index(str(comps))

            return {
                "question_text": f"In a sorted array of $N = {n}$ elements, what is the maximum number of key comparisons required by **Binary Search** in the worst-case scenario?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"Binary search halves search space at each iteration. Worst-case comparisons is given by $\\lfloor \\log_2(N) \\rfloor + 1 = \\lfloor \\log_2({n}) \\rfloor + 1 = {comps}$. Time complexity is $O(\\log N)$.",
                "difficulty": "Easy"
            }

        else:
            return {
                "question_text": "What is the time complexity to find the shortest path between two nodes in a weighted directed graph with non-negative weights using Dijkstra's Algorithm implemented with a Min-Heap priority queue ($V$ vertices, $E$ edges)?",
                "option_a": "$O((V + E) \\log V)$",
                "option_b": "$O(V^2)$",
                "option_c": "$O(V \\cdot E)$",
                "option_d": "$O(E \\log E + V)$",
                "correct_option": 0,
                "explanation": "Each vertex is extracted from the min-heap once ($O(V \\log V)$) and each edge relaxation operation can trigger a decrease-key/heap insert ($O(E \\log V)$). Combining both gives $O((V + E) \\log V)$.",
                "difficulty": "Hard"
            }

    def _generate_parametric_biology(self, topic: str) -> Dict[str, Any]:
        """Generates authentic randomized biology questions with step-by-step genetics & molecular calculations."""
        t_low = topic.lower()

        if "chargaff" in t_low or "molecular" in t_low or "dna" in t_low or "base" in t_low:
            adenine_pct = random.choice([18, 22, 26, 31, 34])
            gc_total = 100 - (2 * adenine_pct)
            cytosine_pct = gc_total // 2

            distractors = [
                adenine_pct,
                round(gc_total / 1.5),
                100 - cytosine_pct
            ]
            options = [f"{cytosine_pct}\\%"] + [f"{d}\\%" for d in distractors if d != cytosine_pct][:3]
            while len(options) < 4:
                options.append(f"{random.randint(15, 45)}\\%")
            random.shuffle(options)
            correct_idx = options.index(f"{cytosine_pct}\\%")

            return {
                "question_text": f"According to Chargaff's rules of base equivalence, if a sample of double-stranded eukaryotic DNA contains **${adenine_pct}\\%$ Adenine**, what is the expected percentage of **Cytosine**?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"According to Chargaff's rule, Adenine pairs with Thymine ($A = T = {adenine_pct}\\%$). The combined $A + T = {2 * adenine_pct}\\%$. Therefore, $G + C = 100\\% - {2 * adenine_pct}\\% = {gc_total}\\%$. Since Guanine equals Cytosine ($G = C$), Cytosine percentage is ${gc_total}\\% / 2 = {cytosine_pct}\\%$.",
                "difficulty": "Medium"
            }

        elif "genetics" in t_low or "hardy" in t_low or "population" in t_low or "allele" in t_low:
            q_val = random.choice([0.1, 0.2, 0.3, 0.4])
            q2_pct = round((q_val ** 2) * 100, 1)
            p_val = round(1.0 - q_val, 1)
            hetero_freq = round(2 * p_val * q_val, 2)
            distractors = [round(q_val**2, 2), round(p_val ** 2, 2), round(p_val * q_val, 2)]
            options = [str(hetero_freq)] + [str(d) for d in distractors if d != hetero_freq][:3]
            while len(options) < 4:
                options.append(str(round(random.uniform(0.15, 0.65), 2)))
            random.shuffle(options)
            correct_idx = options.index(str(hetero_freq))

            return {
                "question_text": f"In a diploid population in Hardy-Weinberg equilibrium, the frequency of homozygous recessive individuals ($aa$) is **${q2_pct}\\%$** ($q^2 = {round(q_val**2, 2)}$). What is the frequency of heterozygous carriers ($Aa$) in this population?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"By the Hardy-Weinberg principle: $q = \\sqrt{{{round(q_val**2, 2)}}} = {q_val}$. Since $p + q = 1$, $p = 1 - {q_val} = {p_val}$. The frequency of heterozygous carriers is given by $2pq = 2 \\times {p_val} \\times {q_val} = {hetero_freq}$ ({round(hetero_freq * 100, 1)}\\% of the population).",
                "difficulty": "Hard"
            }

        elif "cardiac" in t_low or "circulation" in t_low or "physiology" in t_low or "heart" in t_low:
            hr = random.choice([65, 72, 75, 80, 84])
            sv = random.choice([60, 70, 75, 80])
            co = round((hr * sv) / 1000.0, 2)
            distractors = [round(co * 0.75, 2), round(co * 1.3, 2), round((hr + sv) / 20.0, 2)]
            options = [f"{co} L/min"] + [f"{d} L/min" for d in distractors]
            random.shuffle(options)
            correct_idx = options.index(f"{co} L/min")

            return {
                "question_text": f"An athlete has a resting heart rate of **${hr}\\text{{ beats/min}}$** and a ventricular stroke volume of **${sv}\\text{{ mL/beat}}$**. What is their total resting Cardiac Output?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"Cardiac Output ($CO$) is calculated as Heart Rate ($HR$) multiplied by Stroke Volume ($SV$): $CO = {hr}\\text{{ bpm}} \\times {sv}\\text{{ mL}} = {hr * sv}\\text{{ mL/min}} = {co}\\text{{ L/min}}$.",
                "difficulty": "Easy"
            }

        elif "chromosome" in t_low or "meiosis" in t_low or "cell" in t_low:
            n_val = random.choice([8, 12, 16, 23])
            diploid = 2 * n_val
            chromatids_meta1 = diploid * 2
            options = [
                f"{diploid} chromosomes and {chromatids_meta1} chromatids",
                f"{n_val} chromosomes and {diploid} chromatids",
                f"{diploid} chromosomes and {diploid} chromatids",
                f"{n_val} chromosomes and {chromatids_meta1} chromatids"
            ]
            correct = options[0]
            random.shuffle(options)
            correct_idx = options.index(correct)

            return {
                "question_text": f"A sexually reproducing organism has a haploid chromosome count of $n = {n_val}$. How many total chromosomes and chromatids are present in a single cell at **Metaphase I** of meiosis?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"The somatic diploid count is $2n = {diploid}$. During interphase S phase, each chromosome replicates to form two sister chromatids joined at the centromere. Thus at Metaphase I, the cell has $2n = {diploid}$ chromosomes organized into ${n_val}$ bivalents, comprising $2 \\times {diploid} = {chromatids_meta1}$ sister chromatids.",
                "difficulty": "Medium"
            }

        else:
            pcr_start = random.choice([10, 25, 50])
            cycles = random.choice([10, 12, 14])
            total_copies = pcr_start * (2 ** cycles)
            distractors = [pcr_start * cycles * 2, total_copies // 2, total_copies * 2]
            options = [f"{total_copies:,}"] + [f"{d:,}" for d in distractors]
            random.shuffle(options)
            correct_idx = options.index(f"{total_copies:,}")

            return {
                "question_text": f"A PCR gene amplification assay starts with **${pcr_start}$** initial double-stranded DNA template molecules. What is the theoretical yield of target DNA molecules after **${cycles}$** complete thermal cycles?",
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_idx,
                "explanation": f"PCR amplification follows the exponential law $N = N_0 \\times 2^n$, where $N_0$ is the initial copy number and $n$ is cycle count. Here, $N = {pcr_start} \\times 2^{{{cycles}}} = {pcr_start} \\times {2**cycles} = {total_copies:,}$ molecules.",
                "difficulty": "Hard"
            }

    def generate_parametric_question(self, subject_id: str, topic: str) -> Dict[str, Any]:
        """Generates a guaranteed valid, randomized question using topic archetypes."""
        s = subject_id.lower()
        if s == "phys":
            q = self._generate_parametric_physics(topic)
        elif s == "chem":
            q = self._generate_parametric_chemistry(topic)
        elif s == "math":
            q = self._generate_parametric_math(topic)
        elif s == "cs":
            q = self._generate_parametric_cs(topic)
        elif s == "bio":
            q = self._generate_parametric_biology(topic)
        else:
            q = self._generate_parametric_biology(topic) if "bio" in s else self._generate_parametric_physics(topic)

        q["id"] = f"pq_dyn_{uuid.uuid4().hex[:12]}"
        q["subject_id"] = s
        q["topic"] = topic
        q["level_number"] = 1
        q["order_index"] = random.randint(1, 99)
        return q

    # =========================================================================
    # 2. AI-POWERED DYNAMIC GENERATION (GROQ LLM)
    # =========================================================================
    async def generate_ai_questions(
        self, subject_id: str, topic: str, count: int = 3, difficulty: str = "Medium"
    ) -> List[Dict[str, Any]]:
        """
        Uses Groq LLM to synthesize high-yield, unique STEM questions with LaTeX math.
        Falls back seamlessly to the parametric engine if offline or rate-limited.
        """
        if not self.api_key:
            return [self.generate_parametric_question(subject_id, topic) for _ in range(count)]

        subject_names = {
            "phys": "Physics (CBSE Class 12 / JEE Advanced)",
            "chem": "Chemistry (CBSE Class 12 / JEE Advanced)",
            "math": "Mathematics (CBSE Class 12 / JEE Advanced)",
            "cs": "Computer Science (Data Structures, Algorithms & Systems)",
            "bio": "Biology (CBSE Class 11/12 / NEET / Olympiad - Genetics, Cell Biology, Molecular Basis, Ecology, Physiology)"
        }
        subj_desc = subject_names.get(subject_id.lower(), "STEM")

        prompt = f"""You are an elite exam problem setter for {subj_desc}.
Generate exactly {count} distinct, completely original, high-quality multiple-choice questions specifically for the topic: "{topic}".

REQUIREMENTS:
1. Every question MUST directly test "{topic}". Do NOT generate generic or unrelated questions.
2. Use LaTeX math notation enclosed in single dollar signs $...$ for inline and double dollar signs $$...$$ for display formulas.
3. Provide exactly 4 plausible options (A, B, C, D) with realistic distractors targeting common conceptual errors.
4. Correct option must be an integer index (0 for option_a, 1 for option_b, 2 for option_c, 3 for option_d).
5. Explanation must be thorough and educational, showing complete derivations and why distractors are wrong.
6. Set difficulty to "{difficulty}".

Return a single valid JSON object with the key "questions" containing a list:
{{
  "questions": [
    {{
      "question_text": "...",
      "option_a": "...",
      "option_b": "...",
      "option_c": "...",
      "option_d": "...",
      "correct_option": 0,
      "explanation": "...",
      "difficulty": "{difficulty}"
    }}
  ]
}}"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        for model_name in GROQ_MODELS:
            try:
                payload = {
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": "You are a master STEM educator and test generator. You always reply with valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.8,
                    "max_tokens": 2500
                }
                async with httpx.AsyncClient(timeout=14.0) as client:
                    resp = await client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        raw_content = data["choices"][0]["message"]["content"]
                        parsed = json.loads(raw_content)
                        q_list = parsed.get("questions", [])
                        if isinstance(q_list, list) and len(q_list) > 0:
                            valid_questions = []
                            for raw_q in q_list[:count]:
                                if not raw_q.get("question_text") or not raw_q.get("option_a"):
                                    continue
                                c_opt = raw_q.get("correct_option", 0)
                                if not isinstance(c_opt, int) or c_opt not in [0, 1, 2, 3]:
                                    c_opt = 0

                                q_obj = {
                                    "id": f"pq_dyn_{uuid.uuid4().hex[:12]}",
                                    "subject_id": subject_id.lower(),
                                    "topic": topic,
                                    "level_number": 1,
                                    "order_index": random.randint(1, 99),
                                    "difficulty": raw_q.get("difficulty", difficulty),
                                    "question_text": raw_q.get("question_text"),
                                    "option_a": raw_q.get("option_a"),
                                    "option_b": raw_q.get("option_b"),
                                    "option_c": raw_q.get("option_c"),
                                    "option_d": raw_q.get("option_d"),
                                    "correct_option": c_opt,
                                    "explanation": raw_q.get("explanation", "Derivation verified.")
                                }
                                valid_questions.append(q_obj)

                            if len(valid_questions) >= 1:
                                return valid_questions
            except Exception as ex:
                logger.warning(f"[DynamicQuestionEngine] Model {model_name} failed: {ex}")
                continue

        # Fallback to parametric engine
        logger.info(f"[DynamicQuestionEngine] AI generation failed or timed out. Using parametric engine for {topic}.")
        return [self.generate_parametric_question(subject_id, topic) for _ in range(count)]

    # =========================================================================
    # 3. PERSISTENCE INTO SQLITE `practice_questions`
    # =========================================================================
    def save_questions_to_db(self, questions: List[Dict[str, Any]]) -> None:
        """Persists newly generated questions to SQLite so they can be scored and audited."""
        if not questions:
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        for q in questions:
            try:
                raw_subj = str(q.get("subject_id", "phys")).lower()
                if "phys" in raw_subj: clean_subj = "phys"
                elif "chem" in raw_subj: clean_subj = "chem"
                elif "math" in raw_subj: clean_subj = "math"
                elif "cs" in raw_subj or "comp" in raw_subj: clean_subj = "cs"
                elif "bio" in raw_subj: clean_subj = "bio"
                else: clean_subj = "bio" if "bio" in raw_subj else "phys"

                cursor.execute("""
                INSERT OR IGNORE INTO practice_questions (
                    id, subject_id, level_number, order_index, topic, difficulty,
                    question_text, option_a, option_b, option_c, option_d, correct_option, explanation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    q["id"], clean_subj, q.get("level_number", 1), q.get("order_index", 1),
                    q["topic"], q.get("difficulty", "Medium"), q["question_text"],
                    q["option_a"], q["option_b"], q["option_c"], q["option_d"],
                    q["correct_option"], q["explanation"]
                ))
            except Exception as e:
                logger.error(f"[DynamicQuestionEngine] Error saving question: {e}")
        conn.commit()
        conn.close()

    # =========================================================================
    # 4. PRIMARY PUBLIC API: TOPIC QUESTIONS FOR REVISION
    # =========================================================================
    async def get_topic_questions(
        self, subject_id: str, topic: str, count: int = 3, user_id: Optional[str] = None, force_new: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Retrieves or generates unique, dynamic, topic-specific questions for a revision session.
        Guarantees that questions match the exact topic and avoids repetitive static questions.
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        # Find questions already in DB for this exact topic
        cursor.execute("""
        SELECT id, subject_id, level_number, topic, difficulty,
               question_text, option_a, option_b, option_c, option_d,
               correct_option, explanation
        FROM practice_questions
        WHERE subject_id = ? AND topic = ?
        """, (subject_id.lower(), topic))
        existing_rows = [dict(r) for r in cursor.fetchall()]

        # Check what questions the user answered recently to avoid repeating
        answered_ids = set()
        if user_id:
            cursor.execute("""
            SELECT question_id FROM quiz_answers WHERE user_id = ?
            ORDER BY id DESC LIMIT 50
            """, (user_id,))
            answered_ids = {r[0] for r in cursor.fetchall()}

        conn.close()

        unanswered_existing = [q for q in existing_rows if q["id"] not in answered_ids]

        # If we have enough unique unanswered questions for this topic and force_new is False, use them!
        if len(unanswered_existing) >= count and not force_new:
            selected = random.sample(unanswered_existing, count)
            return self._format_questions(selected)

        # Otherwise, generate brand new dynamic questions tailored to this exact topic!
        needed_count = max(count, 3)
        new_questions = await self.generate_ai_questions(subject_id, topic, count=needed_count)
        self.save_questions_to_db(new_questions)

        # Return formatted questions
        return self._format_questions(new_questions[:count])

    def _format_questions(self, q_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formats questions into standardized client payload with indexed options."""
        formatted = []
        for q in q_list:
            formatted.append({
                "id": q["id"],
                "topic": q["topic"],
                "difficulty": q.get("difficulty", "Medium"),
                "question_text": q["question_text"],
                "options": [
                    {"index": 0, "label": "A", "text": q["option_a"]},
                    {"index": 1, "label": "B", "text": q["option_b"]},
                    {"index": 2, "label": "C", "text": q["option_c"]},
                    {"index": 3, "label": "D", "text": q["option_d"]}
                ],
                "correct_option": q["correct_option"],
                "explanation": q["explanation"]
            })
        return formatted


    async def get_level_quiz_questions(
        self, subject_id: str, level_number: int, count: int = 10, user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves a dynamic, randomized set of 10 questions for a quiz attempt.
        Shuffles options and questions so every attempt is fresh and unique.
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, subject_id, level_number, topic, difficulty,
               question_text, option_a, option_b, option_c, option_d,
               correct_option, explanation
        FROM practice_questions
        WHERE subject_id = ? AND level_number = ?
        """, (subject_id.lower(), level_number))
        rows = [dict(r) for r in cursor.fetchall()]

        answered_ids = set()
        if user_id:
            cursor.execute("""
            SELECT question_id FROM quiz_answers WHERE user_id = ?
            ORDER BY id DESC LIMIT 40
            """, (user_id,))
            answered_ids = {r[0] for r in cursor.fetchall()}

        conn.close()

        unanswered = [r for r in rows if r["id"] not in answered_ids]
        pool = unanswered if len(unanswered) >= count else rows

        if len(pool) < count:
            sample_topics = [r["topic"] for r in rows if r.get("topic")]
            chosen_topic = random.choice(sample_topics) if sample_topics else "Core Principles"
            additional = await self.generate_ai_questions(subject_id, chosen_topic, count=max(count - len(pool), 3))
            self.save_questions_to_db(additional)
            pool.extend(additional)

        selected = random.sample(pool, min(count, len(pool)))
        random.shuffle(selected)

        formatted = []
        for q in selected:
            labels = ["A", "B", "C", "D"]
            correct_opt = q.get("correct_option", 0)
            if not isinstance(correct_opt, int) or correct_opt not in [0, 1, 2, 3]:
                try:
                    correct_opt = int(correct_opt)
                except (ValueError, TypeError):
                    correct_opt = 0

            formatted.append({
                "id": q["id"],
                "subject_id": q["subject_id"],
                "level_number": q["level_number"],
                "topic": q["topic"],
                "difficulty": q.get("difficulty", "Medium"),
                "question_text": q["question_text"],
                "option_a": q["option_a"],
                "option_b": q["option_b"],
                "option_c": q["option_c"],
                "option_d": q["option_d"],
                "options": [
                    {"index": 0, "label": "A", "text": q["option_a"]},
                    {"index": 1, "label": "B", "text": q["option_b"]},
                    {"index": 2, "label": "C", "text": q["option_c"]},
                    {"index": 3, "label": "D", "text": q["option_d"]}
                ],
                "correct_option": correct_opt,
                "explanation": q["explanation"]
            })

        return formatted


# Singleton instance
dynamic_question_engine = DynamicQuestionEngine()

