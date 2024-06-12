from manim import *

class Beta(Scene):
    def construct(self):

        #Function returning number of vertices based on the iteration number
        def GetNumberOfVertices(iteration):
            vertices = 3*4**(iteration)
            return vertices
        
        #Function returning all of the new operators based on
        #the previous iteration of operators
        def GetOperators(x_operators, y_operators, iteration):

            new_x_operators = []
            new_y_operators = []

            number_vertices = GetNumberOfVertices(iteration=iteration)

            #Formula for finding the cycle shift, with one exception on iteration 2
            if iteration == 1:
                cycle_shift = 2
            else:
                cycle_shift = 2*4**(iteration-2)

            for _ in range(6):

                #Shift the horizontal operator cycle by 2
                temp = x_operators[:cycle_shift]
                x_operators = x_operators[cycle_shift:]
                x_operators += temp

                operator_group = x_operators[:int(number_vertices / 6)]
                new_x_operators += operator_group

                #Shift the vertical operator cycle by 2
                temp = y_operators[:cycle_shift]
                y_operators = y_operators[cycle_shift:]
                y_operators += temp

                operator_group = y_operators[:int(number_vertices / 6)]
                new_y_operators += operator_group

            return new_x_operators, new_y_operators
        
        #Function returning all of the vertices based on the iteration
        def GetVertices(x_operators, y_operators, iteration):
            vertex = dl
            vertices = [vertex]

            #Get all vertices
            for i in range(GetNumberOfVertices(iteration=iteration)):

                if (i + 1) % 3 != 0:
                    vertex = [vertex[0] + (side_length/2)*x_operators[i], 
                            vertex[1] + height*y_operators[i], 
                            0]
                else:
                    vertex = [vertex[0] + (side_length)*x_operators[i], 
                            vertex[1], 
                            0]

                vertices.append(vertex)
            
            return vertices
        
        #Function for cycling the operators to the correct location
        def CycleOperators(x_operators, y_operators, iteration):
            cycle_shift = 28*4**(iteration-2)

            #Shift horizontal operators to the correct cycle
            temp = x_operators[:cycle_shift]
            x_operators = x_operators[cycle_shift:]
            x_operators += temp

            #Shift vertical operators to the correct cycle
            temp = y_operators[:cycle_shift]
            y_operators = y_operators[cycle_shift:]
            y_operators += temp

            return x_operators, y_operators
        
                
        #Assigns side length and height of the first triangle
        tri = Triangle().scale(2).shift(UP*1.5)

        dl = tri.get_corner(DL)
        dr = tri.get_corner(DR)
        u = tri.get_top()

        side_length = dr[0] - dl[0]
        height = u[1] - dl[1]

        #Keeps track of this inital side length for later
        original_side_length = side_length

        #---ITERATION 0---#
        v1 = dl
        v2 = [v1[0]+side_length/2, v1[1]+height, 0]
        v3 = [v2[0]+side_length/2, v2[1]-height, 0]

        #Create drawing
        iter0 = Polygon(v1, v2, v3, 
                        fill_color=BLUE, fill_opacity=1,
                        stroke_color=WHITE)
        
        #Label iteration
        iter_0_text = Tex(f"Iteration: $0$", font_size=60).to_edge(UP, buff=5)

        self.add(iter0, iter_0_text)


        #---ITERATION 1---#
        side_length /= 3
        height /= 3

        #Pattern: --+-++++-+--
        x_pattern = [-1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1]        

        #Pattern: +O++O+-O--O-
        y_pattern = [1, 0, 1, 1, 0, 1, -1, 0, -1, -1, 0, -1]

        #Get all operators
        x_operators1, y_operators1 = GetOperators(x_operators=x_pattern, y_operators=y_pattern, iteration=1)

        #Get all vertices
        vertices = GetVertices(x_operators=x_operators1, y_operators=y_operators1, iteration=1)
        
        #Create drawing
        iter1 = Polygon(*vertices,
                        fill_color=BLUE, fill_opacity=1,
                        stroke_color=WHITE)
        
        #Label iteration
        iter_1_text = Tex(f"Iteration: $1$", font_size=60).to_edge(UP, buff=5)

        self.play(ReplacementTransform(iter0, iter1),
                  ReplacementTransform(iter_0_text, iter_1_text),
                  run_time=1)

        
        #---ITERATION 2 AND BEYOND---#

        old_x_operators = x_operators1
        old_y_operators = y_operators1
        old_iter = iter1
        old_iter_text = iter_1_text

        #Animates iterations 2-6
        for i in range(5):

            side_length /= 3
            height /= 3

            #Get all the operators
            new_x_operators, new_y_operators = GetOperators(x_operators=old_x_operators, y_operators=old_y_operators, iteration=i+2)

            #Cycle all the operators
            new_x_operators, new_y_operators = CycleOperators(x_operators=new_x_operators, y_operators=new_y_operators, iteration=i+2)

            #Get all the vertices
            vertices = GetVertices(x_operators=new_x_operators, y_operators=new_y_operators, iteration=i+2)

            #Create drawing
            new_iter = Polygon(*vertices,
                            fill_color=BLUE, fill_opacity=1,
                            stroke_color=WHITE)
            
            #Label iteration
            new_iter_text = Tex(f"Iteration: {i+2}", font_size=60).to_edge(UP, buff=5)
            
            
            self.play(ReplacementTransform(old_iter, new_iter), 
                    ReplacementTransform(old_iter_text, new_iter_text),
                    run_time=1)

            #Saves iteration 4 to use later
            if (i+2) == 4:
                iter4 = new_iter.save_state()

            #Reset variables
            old_x_operators = new_x_operators
            old_y_operators = new_y_operators
            old_iter = new_iter
            old_iter_text = new_iter_text
        

        #Iterations diverge to infinity
        iter_n_text = Tex(f"Iteration: $n$", font_size=60).to_edge(UP, buff=5)
        self.play(ReplacementTransform(old_iter_text, iter_n_text))
        self.wait()

        snowflake = old_iter

        #Zoom into Koch Snowflake to show intricacy
        self.play(iter_n_text.animate.shift(DOWN*50),
                  snowflake.animate.scale(10).shift(UP*18),
                  run_time=2)
        self.remove(iter_n_text)
        
        #Zoom out
        self.play(snowflake.animate.scale(1/23).move_to(ORIGIN),
                  run_time=1.5)

        #Makes of a copy of the current snowflake to use for later
        original = snowflake.save_state()
        

        #---TESSELLATIONS---#

        #Restores iteration 4 just to use less memory, because iteration 6 has way too many vertices to do big animations with
        snowflake = iter4.scale(10/23).move_to(ORIGIN)

        for i in range(3):

            run_time = 0.75
            wait_time = 0.25

            #Copies the original snowflake 6 times
            snowflake_copies = [snowflake.copy() for _ in range(6)]

            #Creates an animation group of the snowflakes surrounding the original one diagonally
            diagonal_snowflake_anims = [
                snowflake_copies[0].animate.align_to(snowflake.get_right(), LEFT).align_to(snowflake_copies[0].get_center(), UP).rotate(PI/3),
                snowflake_copies[1].animate.align_to(snowflake.get_left(), RIGHT).align_to(snowflake_copies[1].get_center(), UP).rotate(PI/3),
                snowflake_copies[2].animate.align_to(snowflake.get_left(), RIGHT).align_to(snowflake_copies[2].get_center(), DOWN).rotate(PI/3),
                snowflake_copies[3].animate.align_to(snowflake.get_right(), LEFT).align_to(snowflake_copies[3].get_center(), DOWN).rotate(PI/3)
            ]
            diagonal_snowflake_anims = AnimationGroup(*diagonal_snowflake_anims, lag_ratio=0.1)

            #Creates an animation group of the snowflakes surrounding the original one on the top and bottom
            vertical_snowflake_anims = [
                snowflake_copies[4].animate.align_to(snowflake.get_top(), DOWN).rotate(PI/3),
                snowflake_copies[5].animate.align_to(snowflake.get_bottom(), UP).rotate(PI/3)
            ]
            vertical_snowflake_anims = AnimationGroup(*vertical_snowflake_anims, lag_ratio=0.1)

            #Makes the animations instantaneous after the second iteration
            if i > 1:
                run_time = 0
                wait_time = 0

            #Animation
            self.play(diagonal_snowflake_anims, run_time=run_time)
            self.wait(wait_time)
            self.play(vertical_snowflake_anims, run_time=run_time)
            self.wait(wait_time)

            #Creates bigger snowflake out of smaller snowflakes
            snowflake = VGroup(*snowflake_copies, snowflake)


        #Change the background to pink
        bg = FullScreenRectangle(color=PINK, fill_opacity=0.75)
        self.bring_to_back(bg)
        self.play(FadeIn(bg))

        #Groups the tessellation
        snowflakes = []
        for mob in self.mobjects:
            if not isinstance(mob, Rectangle):
                snowflakes.append(mob)

        #Zooms the tessellation in and out
        self.play(AnimationGroup(*[snowflake.animate.scale(1/5) for snowflake in snowflakes]), run_time=7, rate_func=smoothstep)
        self.play(AnimationGroup(*[snowflake.animate.scale(5) for snowflake in snowflakes]), run_time=4.25, rate_func=smoothstep)

        #Restores the original copy of the snowflake from earlier
        original = original.copy()
        self.add(original)

        #Fades out everything but the center snowflake
        self.play(AnimationGroup(FadeOut(*snowflakes)), FadeOut(bg), run_time=0.25)



        #---EXPANSION AROUND CENTER---#

        #---ITERATION 1---#
        
        #Copies the original snowflake 6 times because there are 6 new snowflakes
        number_of_iter1_snowflakes = 6
        iter1_copies = [original.copy().set_stroke(width=1) for _ in range(number_of_iter1_snowflakes)]

        #How much to move the snowflakes by
        translation_factor = (2/3)*original_side_length*(10/23)

        #Starting direction for the first snowflake
        shift_rotation = PI/3

        #Creates an animation group for all of the snowflakes spiraling from the center
        iterate_from_center = []
        for i in range(number_of_iter1_snowflakes):
            iterate_from_center.append(iter1_copies[i].animate
                                       .scale(1/np.sqrt(3))
                                       .rotate(PI/6)
                                       .shift(RIGHT*translation_factor*np.cos(shift_rotation), UP*translation_factor*np.sin(shift_rotation)))
            
            #Changes the direction that each snowflake is traveling to
            shift_rotation += PI/3

        #Animation
        iterate_from_center = AnimationGroup(*iterate_from_center, lag_ratio=0.1)
        self.play(iterate_from_center)


        #---ITERATION 2---#

        #Keeps track of every snowflake in this new iteration to use for later
        iter2_copies = VGroup()

        #Scales the magnitude of translation down by root 3
        translation_factor *= (1/np.sqrt(3))

        #Starting direction for the first snowflake
        shift_rotation = PI/6

        #Creates an animation group for all of the snowflakes spiraling from the previous iteration
        iterate_from_center = []

        #Iterates 6 times; 18 new snowflakes, with groups of 3 each
        for i in range(number_of_iter1_snowflakes):

            #Copies the original snowflake 3 times to create groups of 3
            snowflake_3_group = [iter1_copies[i].copy().set_stroke(width=0.75) for _ in range(3)]

            #Creates the animations for each individual snowflake in each group of 3
            for j in range(3):
                iterate_from_center.append(snowflake_3_group[j].animate
                                        .scale(1/np.sqrt(3))
                                        .rotate(PI/6)
                                        .shift(RIGHT*translation_factor*np.cos(shift_rotation), UP*translation_factor*np.sin(shift_rotation))
                                        )
                
                #Changes the direction that each snowflake is traveling to
                shift_rotation += PI/3

            #Changes the beginning shift rotation by pi over 3
            shift_rotation -= 2*PI/3

            iter2_copies.add(*snowflake_3_group)

        #Animation              
        iterate_from_center = AnimationGroup(*iterate_from_center, lag_ratio=0.05)
        self.play(iterate_from_center)


        #---ITERATION 3---#

        #Keeps track of every snowflake in this new iteration to use for later
        iter3_copies = VGroup()

        #Scales the magnitude of translation down by root 3
        translation_factor *= (1/np.sqrt(3))

        #Starting direction for the first snowflake
        shift_rotation = -PI/3

        #Creates a repeating pattern for the beginning direction of translation for each group of snowflakes
        shift_rotation_pattern = [ele for _ in range(int(len(iter2_copies)/3)) for ele in [(PI), (2*PI/3), 0]]

        #Creates an animation group for all of the snowflakes spiraling from the previous iteration
        iterate_from_center = []

        #Iterates 18 times; 42 new snowflakes, with groups of 4 each (some snowflakes overlap)
        for i in range(len(iter2_copies)):

            #Skip every third snowflake, as it doesn't need any more copies
            if (i+1) % 3 != 0:

                #Creates the animations for each individual snowflake in each group of 4
                for j in range(4):
                    snowflake_copy = iter2_copies[i].copy().set_stroke(width=0.5)
                    iterate_from_center.append(snowflake_copy.animate
                                            .scale(1/np.sqrt(3))
                                            .rotate(PI/6)
                                            .shift(RIGHT*translation_factor*np.cos(shift_rotation), UP*translation_factor*np.sin(shift_rotation))
                                            )
                    
                    #Changes the direction that each snowflake is traveling to
                    shift_rotation += PI/3

                    iter3_copies.add(snowflake_copy)
            
                #Changes the beginning direction of translation for each group of 4 according to the shift rotation pattern defined earlier
                shift_rotation += shift_rotation_pattern[i]

        #Animation              
        iterate_from_center = AnimationGroup(*iterate_from_center, lag_ratio=0.05)
        self.play(iterate_from_center)


        #---ITERATION 4---#

        #Scales the magnitude of translation down by root 3
        translation_factor *= (1/np.sqrt(3))

        #Starting direction for the first snowflake
        shift_rotation = -PI/2

        #Creates a repeating pattern for the beginning direction of translation for each group of snowflakes
        shift_rotation_pattern = [ele for _ in range(int(len(iter3_copies)/2)) for ele in [(PI), (2*PI/3)]]

        #Creates an animation group for all of the snowflakes spiraling from the previous iteration
        iterate_from_center = []
        
        #Will iterate for however many copies of the snowflake there were in the last iteration
        for i in range(len(iter3_copies)):

            #Won't copy about half of the snowflakes because their position doesn't require them to copy themselves
            match (i+1) % 8:
                case 1 | 2 | 5 | 6:
                
                    #Creates the animations for each individual snowflake in each group of 4
                    for j in range(4):
                        snowflake_copy = iter3_copies[i+1].copy().set_stroke(width=0.25)

                        iterate_from_center.append(snowflake_copy.animate
                                                .scale(1/np.sqrt(3))
                                                .rotate(PI/6)
                                                .shift(RIGHT*translation_factor*np.cos(shift_rotation), UP*translation_factor*np.sin(shift_rotation))
                                                )
                        
                        #Changes the direction that each snowflake is traveling to
                        shift_rotation += PI/3
            
                    #Changes the beginning shift rotation by pi over 3
                    shift_rotation += shift_rotation_pattern[i]

                #1 in every 8 snowflakes needs an extra snowflake
                case 7:
                    shift_rotation += 2*PI/3
                
                    snowflake_copy = iter3_copies[i+1].copy().set_stroke(width=0.25)
                    iterate_from_center.append(snowflake_copy.animate
                                                .scale(1/np.sqrt(3))
                                                .rotate(PI/6)
                                                .shift(RIGHT*translation_factor*np.cos(shift_rotation), UP*translation_factor*np.sin(shift_rotation))
                                                )
                    
                    shift_rotation += PI

        #Animation              
        iterate_from_center = AnimationGroup(*iterate_from_center, lag_ratio=0.05)
        self.play(iterate_from_center)

        iter1_copies = VGroup(*iter1_copies)
        
        

        self.wait()
        
