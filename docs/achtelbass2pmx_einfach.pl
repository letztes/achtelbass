#!/usr/bin/perl

use warnings;
use strict;

#use muster;

## Bevor die Praeambel ausgegeben wird, wird der Notenschluessel abhängig vom verwendeten Notenumfang berechnet.
## Und dafür werden erstmal die Noten definiert. Hier oben sind sie auch leichter zu finden.
#my @noten = qw(e2 f2 g2 a2 b2 c3 d3 e3 f3 g3 a3 b3 c4 d4 e4 f4 g4 a4 b4 c5 d5 e5); # komplett

my $taktaufloesung = 4; # 8 für Achteln etc.
my @intervalle = qw(Prim Sek Terz Quart Quint Sext Sep Okt);
#my @zwei_oder_drei = qw(0 1 1 2 3); # Intervalle. 0 = Prime.
my @zwei_oder_drei = qw(0 1 2 4);
#my @noten = qw(e2 f2 g2 a2 b2 c3 d3 e3 f3 g3 a3 b3 c4 d4 e4 f4);
my @noten = qw(a2 b2 c3 d3 e3 f3 g3 a3 b3 c4 d4 e4 f4 g4);
my $tonart = 'D-Dur'; # Internationale Bezeichnungen. Deutsches H ist hier B; deutsches b ist hier bb.
#my @pause_oder_note = qw(pause note note note note note note);
my @pause_oder_note = qw(note note);
my $notenumfang = @noten;
my $notenindex = int(rand($notenumfang)); # Das ist die erste Note. Nach ihr richtet sich der Notenschluessel.

## Hier fängt die Definition der Praeambelelemente an.
## Zwölf Zahlen stehen als erstes in der Praeambel, durch whitespace getrennt.
## Die ersten acht beschreiben musikalische Daten.
my $anzahl_notensysteme = 1;		# Anzahl der Notensysteme (relativ zu der Anzahl der Instrumente)
my $anzahl_instrumente = 1;		# Anzahl der Instrumente
my $logischer_metrumzaehler = 4;	# Logischer Metrumzähler
my $logischer_metrumnenner = 4;		# Logischer Metrumnenner
my $gedruckter_metrumzaehler = 4;	# Gedruckterer Metrumzähler
my $gedruckter_metrumnenner = 4;	# Gedruckterer Metrumnenner
my $auftaktschlaege = 0;		# Anzahl logischer Schläge im ersten Auftakt. Dezimalbrüche sind möglich.
my $anzahl_vorzeichen = 0;		# Vorzeichen entsprechend dem Quintenzirkel. Positive Zahlen sind Kreuze, negative sind bs.

## Die naechsten vier beschreiben drucktechnische Details.
my $anzahl_seiten = 2;			# Anzahl der Seiten, die das Dokument haben soll
my $anzahl_systeme = 26;		# Anzahl der Notensysteme, d.h. gedruckter Partiturzeilen
my $groesse_system = 16;		# Größe eines Notensystems in pt
my $einrueckung = .1;			# Einrückung in Prozent. 8.5 % schreibt man als .085

## Namen der Instrumente, von unten nach oben.
my $instrumentenbezeichnung = "E-Bass"; # Wird vor das jeweilige Notensystem geschrieben. Kann leergelassen werden.

## Titel des Stücks. Wird zusammengestellt aus den Intervallen und dem
# Notenumfang.
my $titel = "Tt\n";
foreach(sort(@zwei_oder_drei)) {
  $titel .= $intervalle[$_].', ';
}
$titel =~ s/(?:, $)/ in /;
$titel .= $noten[0].' - '.$noten[$#noten];
#$titel .= ' ohne b2';

## Notenschlüssel, von unten nach oben.
# b heißt Bassschlüssel, t heißt Violinschlüssel. Wird in &notenschluessel berechnet.
my $notenschluessel = &notenschluessel();
my $notenschluessel_vormals = $notenschluessel;
#my $notenschluessel = 't';

## Das Verzeichnis, in das die Tex-Datei geschrieben werden soll.
my $verzeichnis = "./\n"; # ./

sub praeambel {
	print "\% PRAEAMBEL\n";
	print $anzahl_notensysteme;
	print " ";
	print $anzahl_instrumente;
	print " ";
	print $logischer_metrumzaehler;
	print " ";
	print $logischer_metrumnenner;
	print " ";
	print $gedruckter_metrumzaehler;
	print " ";
	print $gedruckter_metrumnenner;
	print " ";
	print $auftaktschlaege;
	print " ";
	print $anzahl_vorzeichen;
	print "\n";
	print $anzahl_seiten;
	print " ";
	print $anzahl_systeme;
	print " ";
	print $groesse_system;
	print " ";
	print $einrueckung;
	print "\n";
	print $instrumentenbezeichnung;
	print "\n";
	print $notenschluessel;
	print "\n";
	print $verzeichnis;
	print "\n";
	print $titel;
	print "\n";
}

my @dauern = qw(6 3 1 8 4 2 0);

# Rechtsherum im Quintenzirkel
if ($tonart eq 'C-Dur' || $tonart eq 'a-Moll') {
	$anzahl_vorzeichen = 0;
}
elsif ($tonart eq 'G-Dur' || $tonart eq 'e-Moll') {
	$anzahl_vorzeichen = 1;
}
elsif ($tonart eq 'D-Dur' || $tonart eq 'b-Moll') {
	$anzahl_vorzeichen = 2;
}
elsif ($tonart eq 'A-Dur' || $tonart eq 'fis-Moll') {
	$anzahl_vorzeichen = 3;
}
elsif ($tonart eq 'E-Dur' || $tonart eq 'cis-Moll') {
	$anzahl_vorzeichen = 4;
}
elsif ($tonart eq 'B-Dur' || $tonart eq 'gis-Moll') {
	$anzahl_vorzeichen = 5;
}
# Linksherum im Quintenzirkel
elsif ($tonart eq 'F-Dur' || $tonart eq 'd-Moll') {
	$anzahl_vorzeichen = -1;
}
elsif ($tonart eq 'Bb-Dur' || $tonart eq 'g-Moll') {
	$anzahl_vorzeichen = -2;
}
elsif ($tonart eq 'Es-Dur' || $tonart eq 'c-Moll') {
	$anzahl_vorzeichen = -3;
}
elsif ($tonart eq 'As-Dur' || $tonart eq 'f-Moll') {
	$anzahl_vorzeichen = -4;
}
elsif ($tonart eq 'Des-Dur' || $tonart eq 'bb-Moll') {
	$anzahl_vorzeichen = -5;
}

## Gib die Präambel aus
&praeambel();

## Gib den Korpus aus
&corpus();

sub corpus {
	# Notennamen werden immer klein geschrieben. Dahinter eine Ziffer für die Länge(0,2,4,8,1,3,6)
	# und eine Ziffer für die Oktave(c' hat die Ziffer 4, C hat die Ziffer 3)
	# s steht für sharp(#) und f steht für flat(b). Ganze Note Cis schreibt man also cs03
#	print "\% CORPUS\n";
#	&pattern442_4444_442();

# Gibt die Seitennummer (P = Pagenumber) aus. r = Right. c = Text.
# I ist Anweisung für midi. i ist Instrument, 34 ist mit Plektrum gezupfter Bass.
# K-8-0 ist die Anweisung zum herunteroktavieren. Dabei werden die Noten um eine Oktave tiefer ausgegeben.
# T-12 ist die Anweisung zum Transponieren um 12 Halbtöne nach unten beim Schreiben der Midi-Datei.
print "Prc Ii34T-12 ";
	&complex_pattern();
#	&simple_pattern($notenumfang, $anzahl_systeme, \@noten, $taktaufloesung);
}

sub complex_pattern {
	my $string;
	my @hoch_oder_runter = qw(+ -);
	my $pon = 1; # Pause oder Note
	my $vormals_pon = 0;
	my $richtung;
	my $vormals_richtung = 0; # Irgendwelche Werte sollten drin sein, damit nicht mit undef gearbeitet werden muss.
	my $vor_vormals_richtung = 0;
	
	my $aktuelle_note = $noten[$notenindex];
	my $vormals_note = $aktuelle_note;
	my $vormals_note_nicht_pause = $aktuelle_note;
	my $schritte;
	
	for (1..$anzahl_systeme) {
		for (1..6) { # erster, zweiter, dritter takt
			my $verbleibende_taktdauer = 1;
			my $interne_maximaltaktdauer;

			$interne_maximaltaktdauer = 7 if $taktaufloesung == 64;
			$interne_maximaltaktdauer = 6 if $taktaufloesung == 32;
			$interne_maximaltaktdauer = 5 if $taktaufloesung == 16;
			$interne_maximaltaktdauer = 4 if $taktaufloesung == 8;
			$interne_maximaltaktdauer = 3 if $taktaufloesung == 4;
			$interne_maximaltaktdauer = 2 if $taktaufloesung == 2;
			$interne_maximaltaktdauer = 1 if $taktaufloesung == 1;

			my $interne_maximaltaktdauer_fix = $interne_maximaltaktdauer;
#			my @interne_dauern = qw(6 3 1 8 4 2 0);
			my @interne_dauern = qw(0 2 4 8 1 3 6);
#			my @normale_dauern = qw(64 32 16 8 4 2 1);
			my @normale_dauern = qw(1 2 4 8 16 32 64);
			
			my $schwellenwert = 1-(1/$taktaufloesung);
			my $aktuelle_notendauer;
			my $aktuelle_notendauer_normal;
			while($verbleibende_taktdauer >= (1/$taktaufloesung)) {
#				my $zufallszahl = (int(rand($interne_maximaltaktdauer))+1)/2;
				my $zufallszahl = 1;
				$aktuelle_notendauer = $interne_dauern[($interne_maximaltaktdauer_fix-$zufallszahl)];
				$aktuelle_notendauer_normal = $normale_dauern[($interne_maximaltaktdauer_fix-$zufallszahl)];
				$verbleibende_taktdauer -= (1/$aktuelle_notendauer_normal);

				if ($verbleibende_taktdauer <= $schwellenwert) {
					$schwellenwert = $schwellenwert-((1-$schwellenwert)*2);
					$interne_maximaltaktdauer--;
				}
#				$aktuelle_notendauer = 1 if $aktuelle_notendauer == 16;
#				$aktuelle_notendauer = 3 if $aktuelle_notendauer == 32;
#				$aktuelle_notendauer = 6 if $aktuelle_notendauer == 64;
				
				$vormals_note = $aktuelle_note;
				$aktuelle_note = $noten[$notenindex];
				$schritte = int(rand($#zwei_oder_drei+1));
				# Die folgende Verzweigung stellt sicher, dass nicht zwei Pausen hintereinander
				# auftreten. Ist nämlich witzlos.
				if ($vormals_pon > 0) {
					$pon = int(rand($#pause_oder_note));
					$vormals_pon = $pon;
				}
				else {
					$pon = '1';
					$vormals_pon = $pon;
				}
				
				if ($pause_oder_note[$pon] eq 'pause') {
					$aktuelle_note = 'r'.$aktuelle_notendauer;
				}
				else {
					# Durch die folgende Verzweigung soll die Richtung für mindestens zwei Schritte
					# beibehalten werden.
					if ($vor_vormals_richtung == $vormals_richtung) {
						$richtung = int(rand(2));
						$vor_vormals_richtung = $vormals_richtung;
						$vormals_richtung = $richtung;
					}
					else {
						$vor_vormals_richtung = $vormals_richtung;
						$richtung = $vormals_richtung;					
					}
					# Die folgenden zwei if-Verzweigungen regeln die Richtungsänderung bei
					# Erreichen der Notenumfanggrenze.
          # Dabei ist @zwei_oder_drei = qw(0 1 2 3 1); Intervalle. 0 = Prime.
					if (($notenindex < ($zwei_oder_drei[$schritte]) && $hoch_oder_runter[$richtung] eq '-')) {
						$richtung = 0;
						$vormals_richtung = $richtung;
					}
					if (($notenindex > $notenumfang-($zwei_oder_drei[$schritte]+1) && $hoch_oder_runter[$richtung] eq '+')) {
						$richtung = 1;
						$vormals_richtung = $richtung;
					}
					$notenindex += $zwei_oder_drei[$schritte] if $hoch_oder_runter[$richtung] eq '+';
					$notenindex -= $zwei_oder_drei[$schritte] if $hoch_oder_runter[$richtung] eq '-';
					$aktuelle_note = $noten[$notenindex];
					if ($notenschluessel_vormals ne 't' and (
                        ($vormals_note_nicht_pause =~ /[ab]3$|[cd]4$/ && $aktuelle_note =~ /[defga]4$/)
                        )) {
                        $string .= "Ct ";
                        $notenschluessel_vormals = "t";
          }
					if ($notenschluessel_vormals ne 'b' and (
					              ($vormals_note_nicht_pause =~ /[agfe]3$/ && $aktuelle_note =~ /[edc]3$|[ba]2$/)
                        )) {
                        $string .= "Cb ";
                        $notenschluessel_vormals = "b";
          }
					$vormals_note_nicht_pause = $aktuelle_note if $aktuelle_note !~ /^r/;
    			$vormals_note = $aktuelle_note;
                #    warn "aktuelle note: $aktuelle_note\n\n";
					$aktuelle_note =~ s/(.)$/$aktuelle_notendauer$1/;
				}
				$string .= $aktuelle_note." ";
			}
			$string .= " /\n";
		}
	}
	print $string;
    warn $string;
}

sub notenschluessel {
	my $notenschluessel;
	print "\% index: $notenindex, note: $noten[$notenindex]\n";
	$notenschluessel = 't' if $noten[$notenindex] =~ /[4567]$/;
	$notenschluessel = 'b' if $noten[$notenindex] =~ /[123]$/;
	return $notenschluessel;
}






